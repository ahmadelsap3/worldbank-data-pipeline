#!/usr/bin/env python3
"""
Spotify ETL Pipeline Runner
A simple script to run the complete ETL pipeline for Spotify data.
"""

import os
import sys
import logging
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import ETL functions
from etl_pipeline import extract_spotify_data, transform_data, load_data_to_postgres, verify_data_load

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_etl_pipeline():
    """
    Run the complete ETL pipeline.
    """
    start_time = datetime.now()
    logger.info("Starting Spotify ETL Pipeline")

    try:
        # Extract phase
        logger.info("Starting data extraction...")
        raw_data = extract_spotify_data()
        logger.info(f"Extracted {len(raw_data)} tracks")

        # Transform phase
        logger.info("Starting data transformation...")
        tracks_df, artists_df, albums_df = transform_data(raw_data)
        logger.info(f"Transformed data shape: {tracks_df.shape}")

        # Load phase
        logger.info("Starting data loading...")
        load_data_to_postgres(tracks_df, artists_df, albums_df)
        logger.info("Data loaded successfully")

        # Verification
        logger.info("Verifying data load...")
        verify_data_load()

        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"ETL Pipeline completed successfully in {duration}")

    except Exception as e:
        logger.error(f"ETL Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_etl_pipeline()