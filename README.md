# Spotify ETL Pipeline Project

This project implements an ETL (Extract, Transform, Load) pipeline that extracts data from the Spotify API, transforms and cleans it using Python and Pandas, loads it into a PostgreSQL data warehouse, and can be run manually or automated with scheduling tools. The data can then be consumed by Power BI for visualization and reporting.

## Project Structure

```
├── notebooks/
│   └── spotify_etl.ipynb    # Main ETL notebook (reference implementation)
├── data/
│   ├── raw_tracks.json      # Raw extracted data
│   ├── transformed_tracks.csv
│   ├── transformed_artists.csv
│   └── transformed_albums.csv
├── etl_pipeline.py          # Modular ETL functions
├── run_etl.py              # Simple ETL runner script
├── setup_database.py       # Database setup script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create from .env.example)
├── .env.example            # Environment variables template
├── etl_pipeline.log        # ETL execution logs
└── README.md
```

## Prerequisites

1. **Spotify API Account**: Sign up at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) to get Client ID and Client Secret.

2. **PostgreSQL Database**: Install PostgreSQL locally or use a cloud instance (e.g., AWS RDS, Google Cloud SQL).

3. **Python Environment**: Python 3.8+ with pip.

4. **Virtual Environment**: Recommended to use a virtual environment for dependency isolation.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Data-Exploration-Preparation-and-Visualization-final-project
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Fill in your Spotify API credentials and PostgreSQL details

5. **Set up PostgreSQL database**:
   - Run the database setup script:
   ```bash
   python setup_database.py
   ```

## Usage

### Running the ETL Pipeline

#### Option 1: Run the complete pipeline
```bash
python run_etl.py
```

#### Option 2: Run interactively in Jupyter notebook
```bash
jupyter notebook notebooks/spotify_etl.ipynb
```

#### Option 3: Run individual components
```python
from etl_pipeline import extract_spotify_data, transform_data, load_data_to_postgres

# Extract data
raw_data = extract_spotify_data()

# Transform data
tracks_df, artists_df, albums_df = transform_data(raw_data)

# Load to database
load_data_to_postgres(tracks_df, artists_df, albums_df)
```

### Connecting to Power BI

1. **Install PostgreSQL connector** in Power BI
2. **Create a new data source**:
   - Select PostgreSQL
   - Enter your database credentials from `.env`
3. **Import tables**: `tracks`, `artists`, `albums`
4. **Create visualizations** based on your data

## Data Model

- **artists**: Artist information (id, name, genres, popularity, followers)
- **albums**: Album information (id, name, artist_id, release_date, total_tracks)
- **tracks**: Track details with audio features and foreign keys to artists and albums

## Configuration

### Environment Variables (.env file)
```
# Spotify API Credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here

# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=spotify_etl
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
```

### Getting Spotify API Credentials
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy the Client ID and Client Secret
4. Add them to your `.env` file

## Logging

The ETL pipeline logs all operations to `etl_pipeline.log`. Check this file for detailed execution information and any errors.

## Troubleshooting

### Common Issues
1. **Spotify API errors**: Check your credentials and API quota
2. **Database connection errors**: Verify PostgreSQL is running and credentials are correct
3. **Import errors**: Ensure all dependencies are installed in your virtual environment

### Verification
Run the verification function after loading data:
```python
from etl_pipeline import verify_data_load
verify_data_load()
```

## Next Steps

- Implement incremental loading
- Add more data sources (e.g., audio features)
- Set up monitoring and alerting
- Deploy to production environment
- Add scheduling with cron or other automation tools

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
