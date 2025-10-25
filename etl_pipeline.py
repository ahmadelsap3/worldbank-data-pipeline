"""
Spotify ETL Pipeline Functions
Extract, Transform, Load functions for Spotify data pipeline.
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

def load_config():
    """Load environment variables and return configuration."""
    load_dotenv()

    config = {
        'SPOTIFY_CLIENT_ID': os.getenv('SPOTIFY_CLIENT_ID'),
        'SPOTIFY_CLIENT_SECRET': os.getenv('SPOTIFY_CLIENT_SECRET'),
        'DB_HOST': os.getenv('DB_HOST', 'localhost'),
        'DB_PORT': os.getenv('DB_PORT', '5432'),
        'DB_NAME': os.getenv('DB_NAME', 'spotify_dw'),
        'DB_USER': os.getenv('DB_USER', 'postgres'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'PLAYLIST_ID': os.getenv('PLAYLIST_ID', '37i9dQZF1DXcBWIGoYBM5M')  # Today's Top Hits
    }

    # Validate required credentials
    if not config['SPOTIFY_CLIENT_ID'] or not config['SPOTIFY_CLIENT_SECRET']:
        raise ValueError("Spotify API credentials not found. Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env file")

    if not config['DB_PASSWORD']:
        raise ValueError("Database password not found. Please set DB_PASSWORD in .env file")

    return config

def extract_spotify_data():
    """
    Extract data from Spotify API.

    Returns:
        list: List of track dictionaries
    """
    config = load_config()

    # Authenticate with Spotify
    client_credentials_manager = SpotifyClientCredentials(
        client_id=config['SPOTIFY_CLIENT_ID'],
        client_secret=config['SPOTIFY_CLIENT_SECRET']
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    logger.info("Extracting data from Spotify API...")

    # Extract tracks from playlist
    results = sp.playlist_tracks(config['PLAYLIST_ID'])
    tracks = []

    while results:
        for item in results['items']:
            track = item['track']
            if track:
                track_data = {
                    'track_id': track['id'],
                    'track_name': track['name'],
                    'artist_id': track['artists'][0]['id'] if track['artists'] else None,
                    'artist_name': track['artists'][0]['name'] if track['artists'] else None,
                    'album_id': track['album']['id'],
                    'album_name': track['album']['name'],
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity'],
                    'external_urls': track['external_urls']['spotify'],
                    'extracted_at': datetime.now().isoformat()
                }
                tracks.append(track_data)

        # Get next page
        results = sp.next(results) if results['next'] else None

    logger.info(f"Extracted {len(tracks)} tracks from Spotify")

    # Save raw data for backup
    os.makedirs('data', exist_ok=True)
    with open('data/raw_tracks.json', 'w') as f:
        json.dump(tracks, f, indent=2)

    return tracks

def transform_data(raw_tracks):
    """
    Transform and clean the extracted data.

    Args:
        raw_tracks (list): List of raw track dictionaries

    Returns:
        tuple: (tracks_df, artists_df, albums_df)
    """
    logger.info("Transforming data...")

    # Load raw data into DataFrame
    df_tracks = pd.DataFrame(raw_tracks)

    # Data cleaning
    # Remove duplicates
    df_tracks = df_tracks.drop_duplicates(subset=['track_id'])

    # Handle missing values
    df_tracks = df_tracks.dropna(subset=['track_id', 'track_name'])

    # Convert duration from ms to seconds
    df_tracks['duration_sec'] = df_tracks['duration_ms'] / 1000
    df_tracks = df_tracks.drop('duration_ms', axis=1)

    # Convert extracted_at to datetime
    df_tracks['extracted_at'] = pd.to_datetime(df_tracks['extracted_at'])

    # Create separate DataFrames for artists and albums
    df_artists = df_tracks[['artist_id', 'artist_name']].drop_duplicates().dropna()
    df_albums = df_tracks[['album_id', 'album_name']].drop_duplicates().dropna()

    # Keep only necessary columns for tracks
    df_tracks_clean = df_tracks[['track_id', 'track_name', 'artist_id', 'album_id',
                                'duration_sec', 'popularity', 'external_urls', 'extracted_at']]

    logger.info(f"Transformed data shapes - Tracks: {df_tracks_clean.shape}, Artists: {df_artists.shape}, Albums: {df_albums.shape}")

    # Save transformed data
    os.makedirs('data', exist_ok=True)
    df_tracks_clean.to_csv('data/transformed_tracks.csv', index=False)
    df_artists.to_csv('data/transformed_artists.csv', index=False)
    df_albums.to_csv('data/transformed_albums.csv', index=False)

    return df_tracks_clean, df_artists, df_albums

def load_data_to_postgres(tracks_df, artists_df=None, albums_df=None):
    """
    Load transformed data to PostgreSQL database.

    Args:
        tracks_df (pd.DataFrame): Tracks data
        artists_df (pd.DataFrame): Artists data
        albums_df (pd.DataFrame): Albums data
    """
    config = load_config()

    logger.info("Loading data to PostgreSQL...")

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=config['DB_HOST'],
        port=config['DB_PORT'],
        database=config['DB_NAME'],
        user=config['DB_USER'],
        password=config['DB_PASSWORD']
    )
    cursor = conn.cursor()

    try:
        # Create tables if they don't exist
        create_tables(cursor)
        conn.commit()

        # Load data
        if artists_df is not None and not artists_df.empty:
            load_artists(cursor, artists_df)
        if albums_df is not None and not albums_df.empty:
            load_albums(cursor, albums_df)
        load_tracks(cursor, tracks_df)

        conn.commit()
        logger.info("Data loaded successfully to PostgreSQL")

    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading data: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

def create_tables(cursor):
    """Create database tables if they don't exist."""
    create_artists_table = """
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR(50) PRIMARY KEY,
        artist_name VARCHAR(255) NOT NULL
    );
    """

    create_albums_table = """
    CREATE TABLE IF NOT EXISTS albums (
        album_id VARCHAR(50) PRIMARY KEY,
        album_name VARCHAR(255) NOT NULL
    );
    """

    create_tracks_table = """
    CREATE TABLE IF NOT EXISTS tracks (
        track_id VARCHAR(50) PRIMARY KEY,
        track_name VARCHAR(255) NOT NULL,
        artist_id VARCHAR(50) REFERENCES artists(artist_id),
        album_id VARCHAR(50) REFERENCES albums(album_id),
        duration_sec FLOAT,
        popularity INTEGER,
        external_urls VARCHAR(500),
        extracted_at TIMESTAMP
    );
    """

    cursor.execute(create_artists_table)
    cursor.execute(create_albums_table)
    cursor.execute(create_tracks_table)

def load_artists(cursor, artists_df):
    """Load artists data to database."""
    for _, row in artists_df.iterrows():
        cursor.execute(
            "INSERT INTO artists (artist_id, artist_name) VALUES (%s, %s) ON CONFLICT (artist_id) DO NOTHING",
            (row['artist_id'], row['artist_name'])
        )

def load_albums(cursor, albums_df):
    """Load albums data to database."""
    for _, row in albums_df.iterrows():
        cursor.execute(
            "INSERT INTO albums (album_id, album_name) VALUES (%s, %s) ON CONFLICT (album_id) DO NOTHING",
            (row['album_id'], row['album_name'])
        )

def load_tracks(cursor, tracks_df):
    """Load tracks data to database."""
    for _, row in tracks_df.iterrows():
        cursor.execute(
            """INSERT INTO tracks (track_id, track_name, artist_id, album_id, duration_sec, popularity, external_urls, extracted_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (track_id) DO NOTHING""",
            (row['track_id'], row['track_name'], row['artist_id'], row['album_id'],
             row['duration_sec'], row['popularity'], row['external_urls'], row['extracted_at'])
        )

def verify_data_load():
    """Verify that data has been loaded correctly."""
    config = load_config()

    conn = psycopg2.connect(
        host=config['DB_HOST'],
        port=config['DB_PORT'],
        database=config['DB_NAME'],
        user=config['DB_USER'],
        password=config['DB_PASSWORD']
    )

    try:
        cursor = conn.cursor()

        # Query sample data
        cursor.execute("SELECT COUNT(*) FROM tracks")
        track_count = cursor.fetchone()[0]
        print(f"Total tracks in database: {track_count}")

        cursor.execute("""
            SELECT track_name, artist_name, popularity
            FROM tracks t
            JOIN artists a ON t.artist_id = a.artist_id
            ORDER BY popularity DESC LIMIT 5
        """)
        top_tracks = cursor.fetchall()
        print("\nTop 5 tracks by popularity:")
        for track in top_tracks:
            print(f"{track[0]} by {track[1]} (Popularity: {track[2]})")

    finally:
        cursor.close()
        conn.close()