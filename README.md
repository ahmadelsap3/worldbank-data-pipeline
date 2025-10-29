# Data Exploration, Preparation, and Visualization Pipeline

An automated ETL pipeline for air quality data using **Snowflake**, **dbt**, and **Dagster**, with visualization capabilities in **Power BI**.

## 🏗️ Architecture

```
OpenAQ API (Air Quality Data)
         ↓
    Python Streamer (NDJSON)
         ↓
    Dagster Orchestration
         ↓
Snowflake Data Warehouse
    ├── RAW Schema (raw ingestion)
    ├── RAW_staging Schema (staging views)
    └── RAW_marts Schema (fact tables)
         ├── Staging (stg_openaq)
         ├── Dimensions (dim_station, dim_parameter)
         └── Marts (fact_aq)
         ↓
    Power BI Dashboard
```

## 📋 Prerequisites

- **Python 3.13+** (or 3.9+)
- **Snowflake Account** (Enterprise or higher recommended)
- **Git** (for version control)
- **Power BI Desktop** (optional, for visualization)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ahmadelsap3/Data-Exploration-Preparation-and-Visualization-final-project.git
cd Data-Exploration-Preparation-and-Visualization-final-project
```

### 2. Set Up Python Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file with your Snowflake credentials:

```env
SNOWFLAKE_ACCOUNT=your_account.region
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=ANALYTICS_WH
SNOWFLAKE_DATABASE=ANALYTICS_DB
SNOWFLAKE_SCHEMA=RAW
```

### 4. Run the Pipeline

```bash
python scripts/run_full_pipeline.py
```

This will:
- Provision Snowflake objects (warehouse, database, schemas, tables)
- Generate mock air quality data (100 rows)
- Upload data to Snowflake
- Run dbt transformations
- Create staging views, dimension tables, and fact tables

## 📁 Project Structure

```
Data-Exploration-Preparation-and-Visualization-final-project/
├── scripts/
│   ├── provision_snowflake.py      # Snowflake DDL automation
│   ├── generate_mock_openaq.py     # Mock data generator
│   ├── upload_mock_data.py         # Snowflake data uploader
│   └── run_full_pipeline.py        # Complete pipeline automation
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_openaq.sql      # Staging model
│   │   ├── dimensions/
│   │   │   ├── dim_station.sql     # Station dimension
│   │   │   └── dim_parameter.sql   # Parameter dimension
│   │   └── marts/
│   │       └── fact_aq.sql         # Air quality fact table
│   ├── dbt_project.yml
│   └── profiles.yml                # Located at C:\Users\ahmad\.dbt\profiles.yml
├── orchestration/
│   └── dagster/
│       └── snowflake_uploader.py   # Dagster pipeline
├── data/
│   └── openaq_data.ndjson          # Generated mock data
├── requirements.txt
├── .env                             # Your environment variables
└── README.md
```

## 🔧 Components

### Snowflake Objects

| Object Type | Name | Purpose |
|------------|------|---------|
| Warehouse | `ANALYTICS_WH` | Compute resources (XSMALL, auto-suspend 60s) |
| Database | `ANALYTICS_DB` | Container for all schemas and tables |
| Schema | `RAW` | Raw ingestion layer |
| Schema | `RAW_staging` | Staging layer for transformations |
| Schema | `RAW_marts` | Fact and aggregated tables |
| Table | `OPENAQ_STREAM` | Raw air quality measurements |

### dbt Models

1. **`stg_openaq.sql`** (Staging)
   - Standardizes raw data from `OPENAQ_STREAM` table
   - Creates view in `RAW_staging` schema
   - All columns use quoted identifiers for case sensitivity

2. **`dim_station.sql`** (Dimension)
   - Deduplicates monitoring stations
   - Generates `station_id` using `row_number()`
   - Columns: `station_id`, `station_name`, `city`, `country`, `latitude`, `longitude`

3. **`dim_parameter.sql`** (Dimension)
   - Lists unique measurement parameters (PM2.5, NO2, O3, etc.)
   - Generates `parameter_id` using `row_number()`
   - Columns: `parameter_id`, `parameter_name`, `unit`

4. **`fact_aq.sql`** (Fact Table)
   - Contains all air quality measurements
   - References staging model
   - Schema: `RAW_marts`
   - Columns: `measurement_id`, `location`, `city`, `country`, `parameter`, `value`, `unit`, `latitude`, `longitude`, `measured_at`, `fetched_at`

### Dagster Pipeline

Located in `orchestration/dagster/snowflake_uploader.py`:

- **Job**: `openaq_snowflake_pipeline`
- **Ops**:
  - `check_raw_data` - Verifies NDJSON file exists
  - `stage_openaq_file` - Stages file for Snowflake (PUT command)
  - `upload_openaq_to_snowflake` - Copies staged data into table
  - `verify_upload` - Confirms row count matches

## 📊 Data Schema

The `OPENAQ_STREAM` table contains the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `measurement_id` | NUMBER | Unique measurement identifier |
| `location` | VARCHAR | Station location name |
| `city` | VARCHAR | City name |
| `country` | VARCHAR | Country code |
| `parameter` | VARCHAR | Pollutant type (PM2.5, NO2, O3, etc.) |
| `value` | FLOAT | Measurement value |
| `unit` | VARCHAR | Unit of measurement (µg/m³, ppm) |
| `latitude` | FLOAT | Station latitude |
| `longitude` | FLOAT | Station longitude |
| `measured_at` | TIMESTAMP_NTZ | Measurement timestamp |
| `fetched_at` | TIMESTAMP_NTZ | Data retrieval timestamp |

## 💻 Usage

### Manual Step-by-Step Execution

```bash
# 1. Provision Snowflake objects
python scripts/provision_snowflake.py

# 2. Generate mock data
python scripts/generate_mock_openaq.py

# 3. Upload data to Snowflake
python scripts/upload_mock_data.py

# 4. Run dbt transformations
cd dbt
dbt run
dbt test
```

### Automated Execution

```bash
# Run entire pipeline with one command
python scripts/run_full_pipeline.py
```

### Query Transformed Data

Connect to Snowflake and run:

```sql
-- View all air quality measurements
SELECT * FROM ANALYTICS_DB.RAW_marts.FACT_AQ LIMIT 10;

-- View stations
SELECT * FROM ANALYTICS_DB.RAW.DIM_STATION;

-- View parameters
SELECT * FROM ANALYTICS_DB.RAW.DIM_PARAMETER;

-- Average PM2.5 by city
SELECT 
    "city",
    AVG("value") as avg_pm25
FROM ANALYTICS_DB.RAW_marts.FACT_AQ
WHERE "parameter" = 'pm25'
GROUP BY "city"
ORDER BY avg_pm25 DESC;
```

## 📈 Power BI Integration

### Connecting to Snowflake

1. Open **Power BI Desktop**
2. Click **Get Data** → **Snowflake**
3. Enter connection details:
   - **Server**: `your_account.region.snowflakecomputing.com`
   - **Warehouse**: `ANALYTICS_WH`
   - **Database**: `ANALYTICS_DB`
4. Select **DirectQuery** or **Import** mode
5. Enter your Snowflake credentials
6. Navigate to schemas and select tables:
   - `RAW_marts.FACT_AQ`
   - `RAW.DIM_STATION`
   - `RAW.DIM_PARAMETER`

### Sample Visualizations

1. **Time Series Chart**: PM2.5 trends over time
   - X-axis: `measured_at`
   - Y-axis: `value`
   - Filter: `parameter = 'pm25'`

2. **Map Visual**: Station locations with air quality indicators
   - Latitude: `latitude`
   - Longitude: `longitude`
   - Size: `value`
   - Color: Conditional formatting by AQI thresholds

3. **Bar Chart**: Parameter distribution by city
   - X-axis: `city`
   - Y-axis: Average of `value`
   - Legend: `parameter`

4. **Table**: Daily averages per station
   - Rows: `location`, `city`
   - Values: Average `value`, Max `value`, Min `value`

## 🐛 Troubleshooting

### 1. **Snowflake Connection Errors**

**Problem**: Cannot connect to Snowflake

**Solution**:
- Verify account identifier: `POKMPXO-ICB41863` (yours may differ)
- Check credentials in `.env` file
- Ensure `snowflake-connector-python` is installed: `pip install snowflake-connector-python`

### 2. **dbt Compilation Errors**

**Problem**: `invalid identifier 'COLUMN_NAME'`

**Solution**:
- All column references must use quoted identifiers: `"column_name"`
- Snowflake columns are case-sensitive and lowercase
- Check all dbt models have consistent quoting

**Example Fix**:
```sql
-- ❌ Wrong
SELECT location FROM {{ ref('stg_openaq') }}

-- ✅ Correct
SELECT "location" FROM {{ ref('stg_openaq') }}
```

### 3. **Empty Tables After Upload**

**Problem**: `OPENAQ_STREAM` table has 0 rows

**Solution**:
- Verify `data/openaq_data.ndjson` exists and has content
- Check file path in upload script matches actual location
- Run upload script manually: `python scripts/upload_mock_data.py`
- Query table: `SELECT COUNT(*) FROM ANALYTICS_DB.RAW.OPENAQ_STREAM;`

### 4. **dbt Profile Not Found**

**Problem**: `Profile hotels_egypt_profile not found`

**Solution**:
- Ensure `profiles.yml` exists at `C:\Users\ahmad\.dbt\profiles.yml`
- Verify profile name matches `dbt_project.yml` (should be `hotels_egypt_profile`)
- Check YAML indentation and syntax
- Run `dbt debug` to validate configuration

### 5. **Dagster Pipeline Issues**

**Problem**: Ops don't execute in correct order

**Solution**:
- This is a known issue with the current Dagster configuration
- For now, use manual execution or `run_full_pipeline.py`
- To fix: Add explicit dependencies in Dagster job definition
- Workaround: Run upload script directly before dbt

## 🔨 Development

### Adding New dbt Models

1. Create SQL file in appropriate folder (`models/staging/`, `models/dimensions/`, `models/marts/`)
2. Use `{{ ref('model_name') }}` to reference dependencies
3. Use quoted identifiers for all columns: `"column_name"`
4. Update `dbt/models/schema.yml` with model documentation
5. Run `dbt run --select your_model_name` to test
6. Run `dbt test` to validate data quality

### Adding New Data Sources

1. Create ingestion script in `scripts/`
2. Update `provision_snowflake.py` with new table DDL
3. Create corresponding dbt staging model
4. Update `run_full_pipeline.py` to include new data source

### Scheduling Options

**Option 1: Windows Task Scheduler**
```powershell
# Create scheduled task to run daily at 2 AM
schtasks /create /tn "Air Quality ETL" /tr "C:\path\to\venv\Scripts\python.exe C:\path\to\run_full_pipeline.py" /sc daily /st 02:00
```

**Option 2: Dagster Daemon**
```bash
# Start Dagster daemon for scheduled runs
dagster-daemon run
```

**Option 3: cron (Linux/macOS)**
```bash
# Edit crontab
crontab -e

# Add daily run at 2 AM
0 2 * * * cd /path/to/project && /path/to/venv/bin/python scripts/run_full_pipeline.py
```

## 🔑 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SNOWFLAKE_ACCOUNT` | Snowflake account identifier | `POKMPXO-ICB41863` |
| `SNOWFLAKE_USER` | Snowflake username | `AHMEDEHAB` |
| `SNOWFLAKE_PASSWORD` | Snowflake password | `your_password` |
| `SNOWFLAKE_ROLE` | Snowflake role | `ACCOUNTADMIN` |
| `SNOWFLAKE_WAREHOUSE` | Compute warehouse | `ANALYTICS_WH` |
| `SNOWFLAKE_DATABASE` | Database name | `ANALYTICS_DB` |
| `SNOWFLAKE_SCHEMA` | Default schema | `RAW` |
| `OPENAQ_API_KEY` | OpenAQ API key (optional) | `your_api_key` |

## ✅ Testing

```bash
# Test dbt models
cd dbt
dbt test

# Test Snowflake connection
python -c "from scripts.provision_snowflake import get_snowflake_connection; conn = get_snowflake_connection(); print('✅ Connection successful')"

# Verify data upload
python -c "from scripts.upload_mock_data import verify_upload; verify_upload()"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following the coding standards
4. Test all dbt models: `dbt run && dbt test`
5. Commit your changes: `git commit -m "Add your feature"`
6. Push to the branch: `git push origin feature/your-feature`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **OpenAQ** for providing open air quality data
- **Snowflake** for cloud data warehousing
- **dbt** for data transformation framework
- **Dagster** for orchestration capabilities
