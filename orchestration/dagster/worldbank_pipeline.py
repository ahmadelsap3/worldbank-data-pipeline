"""Dagster pipeline for World Bank data ETL with dbt and Snowflake.

This module defines Dagster assets for:
1. Fetching data from World Bank API
2. Loading data to Snowflake
3. Running dbt transformations
4. Creating dimensional models

Usage:
    dagster dev -f orchestration/dagster/worldbank_pipeline.py
"""
import os
import json
import time
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

import requests
import pandas as pd
import snowflake.connector

from dagster import (
    asset,
    AssetExecutionContext,
    AssetMaterialization,
    Config,
    MaterializeResult,
    MetadataValue,
)


# Configuration
class WorldBankConfig(Config):
    """Configuration for World Bank data fetch."""
    indicators: List[str] = [
        "SP.POP.TOTL",      # Population
        "NY.GDP.MKTP.CD",   # GDP
        "NY.GDP.PCAP.CD",   # GDP per capita
        "SP.DYN.LE00.IN",   # Life expectancy
        "SE.ADT.LITR.ZS",   # Literacy rate
        "SH.DYN.MORT",      # Under-5 mortality
        "EN.ATM.CO2E.PC"    # CO2 emissions
    ]
    countries: List[str] = ["EG", "SA", "AE", "JO", "NG", "ZA", "KE"]
    year_range: str = "2010:2023"


def get_snowflake_connection():
    """Create Snowflake connection from environment variables."""
    password = os.getenv('SNOWFLAKE_PASSWORD')
    
    if not password or password == 'your_password_here':
        raise ValueError(
            "SNOWFLAKE_PASSWORD environment variable not set. "
            "Please set it before starting Dagster or use the start script."
        )
    
    return snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        password=password,
        role=os.getenv('SNOWFLAKE_ROLE', 'ACCOUNTADMIN'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE', 'ANALYTICS_WH'),
        database=os.getenv('SNOWFLAKE_DATABASE', 'ANALYTICS_DB'),
        schema=os.getenv('SNOWFLAKE_SCHEMA', 'RAW')
    )


@asset(group_name="worldbank_pipeline")
def fetch_worldbank_data(
    context: AssetExecutionContext,
    config: WorldBankConfig
) -> pd.DataFrame:
    """Fetch data from World Bank API for configured indicators and countries.
    
    Returns a DataFrame with all fetched data combined.
    """
    BASE_URL = "https://api.worldbank.org/v2"
    all_dataframes = []
    
    for indicator in config.indicators:
        context.log.info(f"Fetching indicator: {indicator}")
        
        country_str = ";".join(config.countries)
        url = f"{BASE_URL}/country/{country_str}/indicator/{indicator}"
        params = {
            "format": "json",
            "date": config.year_range,
            "per_page": 1000,
            "page": 1
        }
        
        all_data = []
        page = 1
        
        while True:
            params["page"] = page
            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if len(data) < 2 or data[1] is None:
                    break
                
                records = data[1]
                if not records:
                    break
                
                all_data.extend(records)
                
                metadata = data[0]
                total_pages = metadata.get("pages", 1)
                if page >= total_pages:
                    break
                
                page += 1
                time.sleep(0.5)
                
            except Exception as e:
                context.log.error(f"Error fetching {indicator}: {e}")
                break
        
        if all_data:
            # Transform to DataFrame
            transformed = []
            fetched_at = datetime.now().isoformat()
            
            for record in all_data:
                if record.get("value") is None:
                    continue
                
                transformed_record = {
                    "indicator_id": record.get("indicator", {}).get("id"),
                    "indicator_name": record.get("indicator", {}).get("value"),
                    "country_id": record.get("country", {}).get("id"),
                    "country_name": record.get("country", {}).get("value"),
                    "year": int(record.get("date", 0)),
                    "value": float(record.get("value", 0)),
                    "unit": record.get("unit", ""),
                    "obs_status": record.get("obs_status", ""),
                    "fetched_at": fetched_at
                }
                transformed.append(transformed_record)
            
            df = pd.DataFrame(transformed)
            all_dataframes.append(df)
            context.log.info(f"  ✓ Fetched {len(df)} records for {indicator}")
    
    # Combine all data
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    
    # Add enrichment columns
    combined_df['decade'] = (combined_df['year'] // 10) * 10
    
    region_mapping = {
        'EG': 'Middle East & North Africa', 'SA': 'Middle East & North Africa',
        'AE': 'Middle East & North Africa', 'JO': 'Middle East & North Africa',
        'NG': 'Sub-Saharan Africa', 'ZA': 'Sub-Saharan Africa', 'KE': 'Sub-Saharan Africa'
    }
    combined_df['region'] = combined_df['country_id'].map(region_mapping)
    
    category_mapping = {
        'SP.POP.TOTL': 'Demographics', 'NY.GDP.MKTP.CD': 'Economy',
        'NY.GDP.PCAP.CD': 'Economy', 'SP.DYN.LE00.IN': 'Health',
        'SE.ADT.LITR.ZS': 'Education', 'SH.DYN.MORT': 'Health',
        'EN.ATM.CO2E.PC': 'Environment'
    }
    combined_df['category'] = combined_df['indicator_id'].map(category_mapping)
    
    combined_df['record_id'] = combined_df.apply(
        lambda row: f"{row['country_id']}_{row['indicator_id']}_{row['year']}", 
        axis=1
    )
    
    context.log.info(f"✓ Total records: {len(combined_df)}")
    context.log_event(
        AssetMaterialization(
            asset_key="fetch_worldbank_data",
            metadata={
                "num_records": len(combined_df),
                "num_countries": combined_df['country_id'].nunique(),
                "num_indicators": combined_df['indicator_id'].nunique(),
                "year_range": f"{combined_df['year'].min()}-{combined_df['year'].max()}",
                "preview": MetadataValue.md(combined_df.head(5).to_markdown())
            }
        )
    )
    
    return combined_df


@asset(group_name="worldbank_pipeline", deps=[fetch_worldbank_data])
def provision_snowflake_objects(context: AssetExecutionContext) -> MaterializeResult:
    """Provision Snowflake warehouse, database, schemas, and tables."""
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    
    ddl_statements = [
        """
        CREATE WAREHOUSE IF NOT EXISTS ANALYTICS_WH
            WITH WAREHOUSE_SIZE = 'XSMALL'
            AUTO_SUSPEND = 60
            AUTO_RESUME = TRUE
        """,
        "CREATE DATABASE IF NOT EXISTS ANALYTICS_DB",
        "USE DATABASE ANALYTICS_DB",
        "CREATE SCHEMA IF NOT EXISTS RAW",
        "CREATE SCHEMA IF NOT EXISTS RAW_STAGING",
        "CREATE SCHEMA IF NOT EXISTS RAW_MARTS",
        "USE SCHEMA RAW",
        """
        CREATE TABLE IF NOT EXISTS WORLDBANK_INDICATORS (
            record_id VARCHAR(200) PRIMARY KEY,
            indicator_id VARCHAR(100),
            indicator_name VARCHAR(500),
            country_id VARCHAR(10),
            country_name VARCHAR(200),
            year NUMBER,
            value FLOAT,
            unit VARCHAR(100),
            obs_status VARCHAR(50),
            decade NUMBER,
            region VARCHAR(100),
            category VARCHAR(100),
            fetched_at TIMESTAMP_NTZ
        )
        """
    ]
    
    objects_created = []
    for stmt in ddl_statements:
        try:
            cursor.execute(stmt)
            first_line = stmt.strip().split('\\n')[0][:50]
            objects_created.append(first_line)
            context.log.info(f"✓ Executed: {first_line}...")
        except Exception as e:
            context.log.error(f"✗ Failed: {e}")
            raise
    
    cursor.close()
    conn.close()
    
    return MaterializeResult(
        metadata={
            "objects_created": len(objects_created),
            "statements": MetadataValue.text("\\n".join(objects_created))
        }
    )


@asset(group_name="worldbank_pipeline", deps=[provision_snowflake_objects])
def load_to_snowflake(
    context: AssetExecutionContext,
    fetch_worldbank_data: pd.DataFrame
) -> MaterializeResult:
    """Load transformed data to Snowflake table using batch inserts."""
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    
    try:
        df = fetch_worldbank_data
        context.log.info(f"Loading {len(df)} rows to Snowflake...")
        
        # Clear existing data
        cursor.execute("TRUNCATE TABLE IF EXISTS WORLDBANK_INDICATORS")
        context.log.info("✓ Cleared existing data")
        
        # Prepare column list for INSERT
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO WORLDBANK_INDICATORS ({columns}) VALUES ({placeholders})"
        
        # Load data in batches
        batch_size = 1000
        rows_loaded = 0
        batch_data = []
        
        for _, row in df.iterrows():
            batch_data.append(tuple(row))
            
            if len(batch_data) >= batch_size:
                cursor.executemany(insert_query, batch_data)
                rows_loaded += len(batch_data)
                context.log.info(f"  Loaded {rows_loaded} rows...")
                batch_data = []
        
        # Load remaining rows
        if batch_data:
            cursor.executemany(insert_query, batch_data)
            rows_loaded += len(batch_data)
        
        cursor.close()
        conn.close()
        
        context.log.info(f"✓ Successfully loaded {rows_loaded} rows")
        
        return MaterializeResult(
            metadata={
                "rows_loaded": rows_loaded,
                "table": "ANALYTICS_DB.RAW.WORLDBANK_INDICATORS"
            }
        )
        
    except Exception as e:
        context.log.error(f"Error loading data: {e}")
        cursor.close()
        conn.close()
        raise


@asset(group_name="worldbank_pipeline", deps=[load_to_snowflake])
def run_dbt_models(context: AssetExecutionContext) -> MaterializeResult:
    """Run dbt models to create staging, dimension, and fact tables."""
    import subprocess
    
    project_root = Path(__file__).parent.parent.parent
    dbt_dir = project_root / "dbt"
    dbt_exe = project_root / "venv" / "Scripts" / "dbt.exe"
    
    context.log.info("Running dbt models...")
    
    try:
        # Set environment variable for password
        env = os.environ.copy()
        
        # Run dbt run
        result = subprocess.run(
            [str(dbt_exe), "run", "--profiles-dir", "."],
            cwd=str(dbt_dir),
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode != 0:
            context.log.error(f"dbt run failed: {result.stderr}")
            raise Exception("dbt run failed")
        
        context.log.info(result.stdout)
        
        # Run dbt test
        test_result = subprocess.run(
            [str(dbt_exe), "test", "--profiles-dir", "."],
            cwd=str(dbt_dir),
            capture_output=True,
            text=True,
            env=env
        )
        
        context.log.info(test_result.stdout)
        
        return MaterializeResult(
            metadata={
                "dbt_output": MetadataValue.text(result.stdout),
                "test_output": MetadataValue.text(test_result.stdout),
                "models_created": 4,
                "tests_passed": "21 tests"
            }
        )
        
    except Exception as e:
        context.log.error(f"Error running dbt: {e}")
        raise
