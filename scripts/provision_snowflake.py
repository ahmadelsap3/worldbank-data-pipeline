"""Provision Snowflake warehouse, database, schemas, and tables for GTFS transit data.

This script creates all necessary Snowflake objects for the public transportation ETL pipeline,
including the GTFS_TRIPS table for Cairo Metro data.

Requires environment variables:
  SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ROLE (optional)
"""
import os
import sys
from pathlib import Path

try:
    import snowflake.connector
except ImportError:
    print("ERROR: snowflake-connector-python is not installed.")
    print("Run: pip install snowflake-connector-python")
    sys.exit(1)


def get_snowflake_connection():
    """Create a Snowflake connection using environment variables."""
    required = ['SNOWFLAKE_ACCOUNT', 'SNOWFLAKE_USER', 'SNOWFLAKE_PASSWORD']
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        print(f"ERROR: Missing required environment variables: {', '.join(missing)}")
        print("Set them before running this script.")
        sys.exit(1)
    
    conn_kwargs = {
        'account': os.getenv('SNOWFLAKE_ACCOUNT'),
        'user': os.getenv('SNOWFLAKE_USER'),
        'password': os.getenv('SNOWFLAKE_PASSWORD'),
        'role': os.getenv('SNOWFLAKE_ROLE', 'ACCOUNTADMIN'),  # Use ACCOUNTADMIN for provisioning
    }
    
    print(f"Connecting to Snowflake account: {conn_kwargs['account']} as {conn_kwargs['user']}")
    return snowflake.connector.connect(**conn_kwargs)


def execute_sql_file(cursor, connection, sql_file: Path):
    """Execute a SQL file, handling multi-statement files."""
    print(f"\n▶ Executing: {sql_file.name}")
    content = sql_file.read_text(encoding='utf-8')
    
    # Remove comment-only lines first
    lines = []
    for line in content.split('\n'):
        stripped = line.strip()
        # Keep non-comment lines and lines that have code before a comment
        if stripped and not stripped.startswith('--'):
            # Remove inline comments
            if '--' in line:
                line = line[:line.index('--')]
            if line.strip():
                lines.append(line)
    
    clean_content = '\n'.join(lines)
    
    # Split by semicolons and preserve order
    statements = []
    for stmt in clean_content.split(';'):
        stmt = stmt.strip()
        if stmt:
            statements.append(stmt)
    
    for i, stmt in enumerate(statements, 1):
        try:
            # Get first line for preview
            first_line = stmt.split('\n')[0].strip()[:60]
            print(f"  → Executing: {first_line}...")
            
            cursor.execute(stmt)
            connection.commit()  # Commit after each statement to ensure objects exist
            print(f"  ✓ Statement {i} completed")
        except Exception as e:
            print(f"  ✗ Statement {i} failed: {e}")
            print(f"    Full statement:\n{stmt[:300]}...")
            raise


def create_gtfs_objects(cursor, connection):
    """Create GTFS-specific Snowflake objects programmatically."""
    
    ddl_statements = [
        # Create warehouse
        """
        CREATE WAREHOUSE IF NOT EXISTS ANALYTICS_WH
            WITH WAREHOUSE_SIZE = 'XSMALL'
            AUTO_SUSPEND = 60
            AUTO_RESUME = TRUE
            INITIALLY_SUSPENDED = TRUE
        """,
        
        # Create database
        "CREATE DATABASE IF NOT EXISTS ANALYTICS_DB",
        
        # Use database
        "USE DATABASE ANALYTICS_DB",
        
        # Create schemas
        "CREATE SCHEMA IF NOT EXISTS RAW",
        "CREATE SCHEMA IF NOT EXISTS RAW_staging",
        "CREATE SCHEMA IF NOT EXISTS RAW_marts",
        
        # Use RAW schema
        "USE SCHEMA RAW",
        
        # Create GTFS trips table
        """
        CREATE TABLE IF NOT EXISTS GTFS_TRIPS (
            trip_id VARCHAR(100) PRIMARY KEY,
            route_id VARCHAR(50),
            route_short_name VARCHAR(50),
            route_long_name VARCHAR(200),
            route_type NUMBER,
            route_color VARCHAR(10),
            direction_id NUMBER,
            direction_name VARCHAR(20),
            service_id VARCHAR(50),
            trip_date DATE,
            departure_time TIME,
            arrival_time TIME,
            origin_stop_id VARCHAR(50),
            origin_stop_name VARCHAR(200),
            origin_lat FLOAT,
            origin_lon FLOAT,
            destination_stop_id VARCHAR(50),
            destination_stop_name VARCHAR(200),
            destination_lat FLOAT,
            destination_lon FLOAT,
            num_stops NUMBER,
            ridership NUMBER,
            delay_minutes NUMBER,
            on_time BOOLEAN,
            generated_at TIMESTAMP_NTZ
        )
        """,
    ]
    
    for i, stmt in enumerate(ddl_statements, 1):
        try:
            # Get first line for preview
            first_line = stmt.strip().split('\n')[0].strip()[:60]
            print(f"  → Executing: {first_line}...")
            
            cursor.execute(stmt)
            connection.commit()
            print(f"  ✓ Statement {i} completed")
        except Exception as e:
            print(f"  ✗ Statement {i} failed: {e}")
            raise


def main():
    print("=" * 70)
    print("Snowflake Provisioning Script - GTFS Transit Data")
    print("=" * 70)
    
    # Connect and execute
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    
    try:
        print("\nCreating Snowflake objects for GTFS data...")
        create_gtfs_objects(cursor, conn)
        
        conn.commit()
        print("\n" + "=" * 70)
        print("✓ Snowflake provisioning completed successfully!")
        print("=" * 70)
        print("\nCreated:")
        print("  - Warehouse: ANALYTICS_WH (XSMALL, auto-suspend 60s)")
        print("  - Database: ANALYTICS_DB")
        print("  - Schemas: RAW, RAW_staging, RAW_marts")
        print("  - Table: ANALYTICS_DB.RAW.GTFS_TRIPS")
        print("    - 24 columns for transit trip data")
        print("    - Supports Cairo Metro Lines 1, 2, 3")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Provisioning failed: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()
