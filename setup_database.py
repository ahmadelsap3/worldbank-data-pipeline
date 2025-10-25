#!/usr/bin/env python3
"""
Database Setup Script for Spotify ETL Pipeline
Run this script to create the PostgreSQL database and tables.
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    """Create the PostgreSQL database and tables."""

    # Database connection parameters
    db_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': 'postgres'  # Connect to default database first
    }

    try:
        # Connect to PostgreSQL
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cursor = conn.cursor()

        # Create database if it doesn't exist
        db_name = os.getenv('DB_NAME', 'spotify_etl')
        print(f"Creating database '{db_name}' if it doesn't exist...")
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully!")
        else:
            print(f"Database '{db_name}' already exists.")

        # Close connection to default database
        cursor.close()
        conn.close()

        # Connect to the new database
        db_params['database'] = db_name
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Create tables
        print("Creating tables...")

        # Artists table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artists (
                artist_id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                genres TEXT[],
                popularity INTEGER,
                followers INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Albums table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS albums (
                album_id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                artist_id VARCHAR(255) REFERENCES artists(artist_id),
                release_date DATE,
                total_tracks INTEGER,
                album_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tracks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                track_id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                artist_id VARCHAR(255) REFERENCES artists(artist_id),
                album_id VARCHAR(255) REFERENCES albums(album_id),
                duration_ms INTEGER,
                popularity INTEGER,
                explicit BOOLEAN,
                danceability DECIMAL(3,2),
                energy DECIMAL(3,2),
                key INTEGER,
                loudness DECIMAL(5,2),
                mode INTEGER,
                speechiness DECIMAL(3,2),
                acousticness DECIMAL(3,2),
                instrumentalness DECIMAL(3,2),
                liveness DECIMAL(3,2),
                valence DECIMAL(3,2),
                tempo DECIMAL(5,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tracks_artist_id ON tracks(artist_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tracks_album_id ON tracks(album_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_albums_artist_id ON albums(artist_id)")

        conn.commit()
        print("All tables created successfully!")

        cursor.close()
        conn.close()

        print("\nDatabase setup completed successfully!")
        print(f"Database: {db_name}")
        print("Tables created: artists, albums, tracks")

    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        raise

if __name__ == "__main__":
    create_database()