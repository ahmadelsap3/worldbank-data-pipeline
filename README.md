# World Bank Data Pipeline# World Bank Data Pipeline# World Bank Data Pipeline# World Bank Data Pipeline



An automated ETL pipeline that fetches World Bank development indicators, loads them into Snowflake, transforms the data using dbt, and orchestrates everything with Dagster.



## ArchitectureAn automated ETL pipeline that fetches World Bank development indicators, loads them into Snowflake, transforms the data using dbt, and orchestrates the entire process with Dagster.



```

World Bank API

      ↓## 🏗️ ArchitectureAn automated ETL pipeline that fetches World Bank development indicators, loads them into Snowflake, transforms the data using dbt, and orchestrates the entire process with Dagster.An automated ETL pipeline that fetches World Bank development indicators, loads them into Snowflake, transforms the data using dbt, and orchestrates the entire process with Dagster.

Python (Pandas)

      ↓

Snowflake

  ├── RAW```

  ├── RAW_STAGING  

  └── RAW_MARTSWorld Bank API

      ↓

dbt Transformations      ↓## 🏗️ Architecture

      ↓

Dagster OrchestrationPython ETL (Pandas)

```

      ↓

## Prerequisites

Snowflake Data Warehouse

- Python 3.9+

- Snowflake Account  ├── RAW Schema```This project implements a complete ETL pipeline for World Bank development indicators using:## 🏗️ Architecture

- Git

  ├── RAW_STAGING Schema

## Quick Start

  └── RAW_MARTS SchemaWorld Bank API

### 1. Clone Repository

      ↓

```bash

git clone https://github.com/ahmadelsap3/worldbank-data-pipeline.gitdbt Transformations      ↓- **Extraction**: World Bank Open Data API

cd worldbank-data-pipeline

```  ├── Staging



### 2. Setup Python Environment  ├── DimensionsPython ETL (Pandas)



```bash  └── Marts

python -m venv venv

      ↓      ↓- **Transformation**: dbt (data build tool)```

# Windows

venv\Scripts\activateDagster Orchestration



# macOS/Linux```Snowflake Data Warehouse

source venv/bin/activate



# Install packages

pip install -r requirements.txt## 📋 Prerequisites  ├── RAW Schema (raw tables)- **Loading**: Snowflake data warehouseOpenAQ API (Air Quality Data)

```



### 3. Configure Snowflake Credentials

- Python 3.13+ (or 3.9+)  ├── RAW_STAGING Schema (staging views)

Copy `.env.example` to `.env` and add your credentials:

- Snowflake Account

```bash

# Windows- Git  └── RAW_MARTS Schema (fact tables)- **Orchestration**: Dagster         ↓

copy .env.example .env



# macOS/Linux  

cp .env.example .env## 🚀 Quick Start      ↓

```



Edit `.env`:

### 1. Clone the Repositorydbt Transformations    Python Streamer (NDJSON)

```env

SNOWFLAKE_ACCOUNT=your_account.region

SNOWFLAKE_USER=your_username

SNOWFLAKE_PASSWORD=your_password```bash  ├── Staging: stg_worldbank

SNOWFLAKE_ROLE=ACCOUNTADMIN

SNOWFLAKE_WAREHOUSE=ANALYTICS_WHgit clone https://github.com/ahmadelsap3/air-quality-etl-pipeline.git

SNOWFLAKE_DATABASE=ANALYTICS_DB

SNOWFLAKE_SCHEMA=RAWcd air-quality-etl-pipeline  ├── Dimensions: dim_country, dim_indicator## 🚀 Quick Start         ↓

```

```

### 4. Run Pipeline

  └── Marts: fact_worldbank

**Option A: Jupyter Notebook (Recommended)**

### 2. Set Up Python Environment

```bash

jupyter notebook notebooks/worldbank_data_pipeline.ipynb      ↓    Dagster Orchestration

```

```bash

Execute all cells to fetch data, load to Snowflake, and transform with dbt.

# Create and activate virtual environmentDagster Orchestration

**Option B: Dagster (Automated)**

python -m venv venv

```bash

dagster dev -f orchestration/dagster/worldbank_pipeline.py```### 1. Configure Environment         ↓

```

# Windows

Open http://localhost:3000 and click "Materialize all".

venv\Scripts\activate

### 5. Verify Data



```sql

-- Check row counts# macOS/Linux## 📋 PrerequisitesSnowflake Data Warehouse

SELECT COUNT(*) FROM ANALYTICS_DB.RAW.WORLDBANK_INDICATORS;  -- ~600+ rows

SELECT COUNT(*) FROM ANALYTICS_DB.RAW.DIM_COUNTRY;            -- 7 rowssource venv/bin/activate

SELECT COUNT(*) FROM ANALYTICS_DB.RAW.DIM_INDICATOR;          -- 7 rows

SELECT COUNT(*) FROM ANALYTICS_DB.RAW_MARTS.FACT_WORLDBANK;  -- ~600+ rows

```

# Install dependencies

## Project Structure

pip install -r requirements.txt- **Python 3.13+** (or 3.9+)Create `.env` file:    ├── RAW Schema (raw ingestion)

```

worldbank-data-pipeline/```

├── .env                    # Your credentials (not in Git)

├── .env.example            # Template- **Snowflake Account**

├── requirements.txt        # Python packages

├── notebooks/### 3. Configure Environment Variables

│   └── worldbank_data_pipeline.ipynb

├── dbt/- **Git**```env    ├── RAW_staging Schema (staging views)

│   ├── models/

│   │   ├── staging/stg_worldbank.sqlCreate a `.env` file in the project root:

│   │   ├── dimensions/dim_country.sql

│   │   ├── dimensions/dim_indicator.sql

│   │   └── marts/fact_worldbank.sql

│   └── profiles.yml```env

├── orchestration/

│   └── dagster/worldbank_pipeline.pySNOWFLAKE_ACCOUNT=your_account.region## 🚀 Quick StartSNOWFLAKE_ACCOUNT=your_account    └── RAW_marts Schema (fact tables)

└── venv/                   # Python environment

```SNOWFLAKE_USER=your_username



## Data DetailsSNOWFLAKE_PASSWORD=your_password



### Fetched DataSNOWFLAKE_ROLE=ACCOUNTADMIN



- **7 Countries**: Egypt, Saudi Arabia, UAE, Jordan, Nigeria, South Africa, KenyaSNOWFLAKE_WAREHOUSE=ANALYTICS_WH### 1. Clone the RepositorySNOWFLAKE_USER=your_username         ├── Staging (stg_openaq)

- **7 Indicators**: Population, GDP, Life Expectancy, Infant Mortality, Literacy Rate, CO2 Emissions, Electricity Access

- **Years**: 2010-2023SNOWFLAKE_DATABASE=ANALYTICS_DB

- **Records**: ~600+

SNOWFLAKE_SCHEMA=RAW

### Snowflake Objects

```

| Object | Schema | Description |

|--------|--------|-------------|```bashSNOWFLAKE_PASSWORD=your_password         ├── Dimensions (dim_station, dim_parameter)

| WORLDBANK_INDICATORS | RAW | Raw API data |

| STG_WORLDBANK | RAW_STAGING | Cleaned staging view |**Note:** The `.env` file is already in `.gitignore` and will not be uploaded to GitHub.

| DIM_COUNTRY | RAW | Country dimension (7 rows) |

| DIM_INDICATOR | RAW | Indicator dimension (7 rows) |git clone https://github.com/ahmadelsap3/air-quality-etl-pipeline.git

| FACT_WORLDBANK | RAW_MARTS | Analytics fact table |

### 4. Run the Pipeline

### dbt Models

cd air-quality-etl-pipelineSNOWFLAKE_ROLE=ACCOUNTADMIN         └── Marts (fact_aq)

1. **stg_worldbank** - Staging view with null filtering

2. **dim_country** - Deduplicated countries with surrogate keys**Option A: Using Jupyter Notebook (Interactive)**

3. **dim_indicator** - Deduplicated indicators with metadata

4. **fact_worldbank** - Main analytics table```



## Query Examples```bash



```sqljupyter notebook notebooks/worldbank_data_pipeline.ipynbSNOWFLAKE_WAREHOUSE=ANALYTICS_WH         ↓

-- GDP trends for Egypt

SELECT YEAR, VALUE as GDP```

FROM ANALYTICS_DB.RAW_MARTS.FACT_WORLDBANK

WHERE COUNTRY_NAME = 'Egypt' ### 2. Set Up Python Environment

  AND INDICATOR_NAME = 'GDP (current US$)'

ORDER BY YEAR DESC;Execute all cells to:



-- Life expectancy comparison (2023)- Fetch World Bank data for 7 countries and 7 indicators (2010-2023)SNOWFLAKE_DATABASE=ANALYTICS_DB    Power BI Dashboard

SELECT COUNTRY_NAME, VALUE as LIFE_EXPECTANCY

FROM ANALYTICS_DB.RAW_MARTS.FACT_WORLDBANK- Transform and enrich the data

WHERE INDICATOR_NAME = 'Life expectancy at birth, total (years)'

  AND YEAR = 2023- Load ~600+ records into Snowflake```bash

ORDER BY VALUE DESC;

```



## Troubleshooting**Option B: Using Dagster (Automated)**# Create and activate virtual environmentSNOWFLAKE_SCHEMA=RAW```



### Can't connect to Snowflake

- Verify credentials in `.env`

- Check account identifier format: `account.region````bashpython -m venv venv

- Ensure ACCOUNTADMIN role or sufficient permissions

dagster dev -f orchestration/dagster/worldbank_pipeline.py

### dbt errors

- Column names are case-sensitive in Snowflake```venv\Scripts\activate  # Windows```

- All models use UPPERCASE column references

- Run `dbt debug` to check configuration



### Package errorsThen open http://localhost:3000 and click **"Materialize all"** to run the complete pipeline.# source venv/bin/activate  # macOS/Linux

- Activate virtual environment: `venv\Scripts\activate`

- Reinstall: `pip install -r requirements.txt`



### Dagster won't start### 5. Run dbt Transformations## 📋 Prerequisites

- Ensure `.env` file exists with password

- Check if port 3000 is in use

- Try different port: `dagster dev -f orchestration/dagster/worldbank_pipeline.py -p 3001`

```bash# Install dependencies

## Documentation

cd dbt

See [SETUP.md](SETUP.md) for detailed setup instructions and troubleshooting.

dbt runpip install -r requirements.txt### 2. Run the Pipeline

## Contributing

dbt test

1. Fork the repository

2. Create feature branch``````

3. Test changes (dbt run && dbt test)

4. Submit pull request



## LicenseThis creates:- **Python 3.13+** (or 3.9+)



Educational purposes only.- **Staging view**: STG_WORLDBANK



## Credits- **Dimension tables**: DIM_COUNTRY, DIM_INDICATOR### 3. Configure Environment Variables



- **World Bank Open Data** - Development indicators API- **Fact table**: FACT_WORLDBANK

- **Snowflake** - Cloud data warehouse

- **dbt** - Data transformations**Option A: Interactive Notebook**- **Snowflake Account** (Enterprise or higher recommended)

- **Dagster** - Pipeline orchestration

## 📁 Project Structure

Create a `.env` file in the project root:

```

air-quality-etl-pipeline/```bash- **Git** (for version control)

├── .env                           # Environment variables (not in Git)

├── .gitignore                     # Git ignore rules```env

├── requirements.txt               # Python dependencies

├── notebooks/SNOWFLAKE_ACCOUNT=your_account.regionjupyter notebook notebooks/worldbank_data_pipeline.ipynb- **Power BI Desktop** (optional, for visualization)

│   └── worldbank_data_pipeline.ipynb

├── dbt/SNOWFLAKE_USER=your_username

│   ├── dbt_project.yml

│   ├── profiles.ymlSNOWFLAKE_PASSWORD=your_password```

│   └── models/

│       ├── staging/SNOWFLAKE_ROLE=ACCOUNTADMIN

│       │   └── stg_worldbank.sql

│       ├── dimensions/SNOWFLAKE_WAREHOUSE=ANALYTICS_WH## 🚀 Quick Start

│       │   ├── dim_country.sql

│       │   └── dim_indicator.sqlSNOWFLAKE_DATABASE=ANALYTICS_DB

│       └── marts/

│           └── fact_worldbank.sqlSNOWFLAKE_SCHEMA=RAW**Option B: Automated with Dagster**

├── orchestration/

│   └── dagster/```

│       └── worldbank_pipeline.py

├── data/```bash### 1. Clone the Repository

│   └── gtfs_data.ndjson

└── venv/                          # Active Python environment> **Note**: The `.env` file is already in `.gitignore` and will not be uploaded to GitHub.

```

dagster dev -f orchestration/dagster/worldbank_pipeline.py

## 📊 Data Pipeline Details

### 4. Run the Pipeline

### Data Fetched

``````bash

- **7 Indicators**: Population, GDP, Life Expectancy, Infant Mortality, Literacy Rate, CO2 Emissions, Access to Electricity

- **7 Countries**: Egypt, Saudi Arabia, UAE, Jordan, Nigeria, South Africa, Kenya**Option A: Using Jupyter Notebook (Interactive)**

- **Time Range**: 2010-2023

- **Total Records**: ~600+ measurementsgit clone https://github.com/ahmadelsap3/Data-Exploration-Preparation-and-Visualization-final-project.git



### Snowflake Objects Created```bash



| Object | Schema | Description |jupyter notebook notebooks/worldbank_data_pipeline.ipynbThen open http://localhost:3000 and materialize the assets.cd Data-Exploration-Preparation-and-Visualization-final-project

|--------|--------|-------------|

| WORLDBANK_INDICATORS | RAW | Raw data table |```

| STG_WORLDBANK | RAW_STAGING | Cleaned staging view |

| DIM_COUNTRY | RAW | Country dimension |```

| DIM_INDICATOR | RAW | Indicator dimension |

| FACT_WORLDBANK | RAW_MARTS | Analytics fact table |Execute all cells to:



### dbt Models## 📊 What Gets Created



1. **stg_worldbank**: Staging view that filters null values- Fetch World Bank data for 7 countries and 7 indicators (2010-2023)

2. **dim_country**: Deduplicated country dimension with surrogate keys

3. **dim_indicator**: Deduplicated indicator dimension with metadata- Transform and enrich the data### 2. Set Up Python Environment

4. **fact_worldbank**: Main fact table for analysis

- Load ~600+ records into Snowflake

## 🔧 Dagster Pipeline

- **7 indicators** (Population, GDP, Life Expectancy, etc.)

The pipeline consists of 4 assets:

**Option B: Using Dagster (Automated)**

1. **fetch_worldbank_data**: Fetches data from World Bank API

2. **provision_snowflake_objects**: Creates warehouse, database, schemas, tables- **7 countries** (Egypt, Saudi Arabia, UAE, Jordan, Nigeria, South Africa, Kenya)```bash

3. **load_to_snowflake**: Loads data using batch inserts (1000 rows/batch)

4. **run_dbt_models**: Executes dbt transformations```bash



## 💻 Query Examplesdagster dev -f orchestration/dagster/worldbank_pipeline.py- **2010-2023** time rangepython -m venv venv



```sql```

-- View all countries

SELECT * FROM ANALYTICS_DB.RAW.DIM_COUNTRY;- **~600+ records** loaded to Snowflakevenv\Scripts\activate  # On Windows



-- View all indicatorsThen open http://localhost:3000 in your browser and click "Materialize all" to run the complete pipeline.

SELECT * FROM ANALYTICS_DB.RAW.DIM_INDICATOR;

- **4 dbt models**: staging → dimensions → fact tablepip install -r requirements.txt

-- Get GDP trends for Egypt

SELECT ### 5. Run dbt Transformations

    YEAR,

    VALUE as GDP```

FROM ANALYTICS_DB.RAW_MARTS.FACT_WORLDBANK

WHERE COUNTRY_NAME = 'Egypt' ```bash

  AND INDICATOR_NAME = 'GDP (current US$)'

ORDER BY YEAR DESC;cd dbt## 🔗 Documentation



-- Compare life expectancy across countries in 2023dbt run

SELECT 

    COUNTRY_NAME,dbt test### 3. Configure Environment Variables

    VALUE as LIFE_EXPECTANCY

FROM ANALYTICS_DB.RAW_MARTS.FACT_WORLDBANK```

WHERE INDICATOR_NAME = 'Life expectancy at birth, total (years)'

  AND YEAR = 2023- See `WORLDBANK_QUICKSTART.md` for detailed setup

ORDER BY VALUE DESC;

```This creates:



## 🐛 Troubleshooting- See `PIPELINE_README.md` (this file) for architecture detailsCreate a `.env` file with your Snowflake credentials:



### Dagster won't start- **Staging view**: `STG_WORLDBANK` (cleans and standardizes data)



Ensure password is set in `.env` file and run:- **Dimension tables**: `DIM_COUNTRY`, `DIM_INDICATOR`



```bash- **Fact table**: `FACT_WORLDBANK` (analytics-ready data)

dagster dev -f orchestration/dagster/worldbank_pipeline.py

```## 📁 Key Files```env



### dbt column name errors## 📁 Project Structure



Snowflake column names are case-sensitive. All dbt models use UPPERCASE column references.SNOWFLAKE_ACCOUNT=your_account.region



### Snowflake connection issues```



Verify your `.env` file has:air-quality-etl-pipeline/- `notebooks/worldbank_data_pipeline.ipynb` - Interactive explorationSNOWFLAKE_USER=your_username

- Correct account identifier (format: `account.region`)

- Valid username and password├── .env                          # Environment variables (not in Git)

- Role with sufficient permissions (ACCOUNTADMIN recommended)

├── .gitignore                    # Git ignore rules- `orchestration/dagster/worldbank_pipeline.py` - Automated pipelineSNOWFLAKE_PASSWORD=your_password

### Python package errors

├── requirements.txt              # Python dependencies

Ensure you're using the correct virtual environment:

│- `dbt/models/` - Data transformations (SQL)SNOWFLAKE_ROLE=ACCOUNTADMIN

```bash

# Activate venv├── notebooks/

venv\Scripts\activate  # Windows

source venv/bin/activate  # macOS/Linux│   └── worldbank_data_pipeline.ipynb  # Interactive ETL notebookSNOWFLAKE_WAREHOUSE=ANALYTICS_WH



# Reinstall if needed│SNOWFLAKE_DATABASE=ANALYTICS_DB

pip install -r requirements.txt

```├── dbt/SNOWFLAKE_SCHEMA=RAW



## 🔑 Environment Variables│   ├── dbt_project.yml          # dbt configuration```



| Variable | Description | Example |│   ├── profiles.yml             # Snowflake connection config

|----------|-------------|---------|

| SNOWFLAKE_ACCOUNT | Account identifier | POKMPXO-ICB41863 |│   └── models/### 4. Run the Pipeline

| SNOWFLAKE_USER | Username | AHMEDEHAB |

| SNOWFLAKE_PASSWORD | Password | your_secure_password |│       ├── staging/

| SNOWFLAKE_ROLE | Role | ACCOUNTADMIN |

| SNOWFLAKE_WAREHOUSE | Warehouse name | ANALYTICS_WH |│       │   └── stg_worldbank.sql     # Staging view```bash

| SNOWFLAKE_DATABASE | Database name | ANALYTICS_DB |

| SNOWFLAKE_SCHEMA | Default schema | RAW |│       ├── dimensions/python scripts/run_full_pipeline.py



## 📈 Next Steps│       │   ├── dim_country.sql       # Country dimension```



- Add scheduling with Dagster sensors or schedules│       │   └── dim_indicator.sql     # Indicator dimension

- Extend indicator list in the notebook

- Connect Power BI or Tableau for visualizations│       └── marts/This will:

- Implement custom dbt data quality tests

- Set up CI/CD with GitHub Actions│           └── fact_worldbank.sql    # Fact table- Provision Snowflake objects (warehouse, database, schemas, tables)



## 🤝 Contributing│- Generate mock air quality data (100 rows)



1. Fork the repository├── orchestration/- Upload data to Snowflake

2. Create a feature branch

3. Make your changes│   └── dagster/- Run dbt transformations

4. Test thoroughly (dbt run && dbt test)

5. Submit a pull request│       └── worldbank_pipeline.py     # Dagster orchestration- Create staging views, dimension tables, and fact tables



## 📝 License│



This project is for educational purposes.├── data/## 📁 Project Structure



## 🙏 Acknowledgments│   └── gtfs_data.ndjson         # Sample data files



- **World Bank Open Data** - Development indicators API│```

- **Snowflake** - Cloud data warehousing

- **dbt** - SQL-based transformations└── venv/                        # Python virtual environment (active)Data-Exploration-Preparation-and-Visualization-final-project/

- **Dagster** - Modern data orchestration

```├── scripts/

│   ├── provision_snowflake.py      # Snowflake DDL automation

## 📊 Data Pipeline Details│   ├── generate_mock_openaq.py     # Mock data generator

│   ├── upload_mock_data.py         # Snowflake data uploader

### Data Fetched│   └── run_full_pipeline.py        # Complete pipeline automation

├── dbt/

- **7 Indicators**: Population, GDP, Life Expectancy, Infant Mortality, Literacy Rate, CO2 Emissions, Access to Electricity│   ├── models/

- **7 Countries**: Egypt, Saudi Arabia, UAE, Jordan, Nigeria, South Africa, Kenya│   │   ├── staging/

- **Time Range**: 2010-2023│   │   │   └── stg_openaq.sql      # Staging model

- **Total Records**: ~600+ measurements│   │   ├── dimensions/

│   │   │   ├── dim_station.sql     # Station dimension

### Snowflake Objects Created│   │   │   └── dim_parameter.sql   # Parameter dimension

│   │   └── marts/

| Object | Schema | Description |│   │       └── fact_aq.sql         # Air quality fact table

|--------|--------|-------------|│   ├── dbt_project.yml

| `WORLDBANK_INDICATORS` | RAW | Raw data table |│   └── profiles.yml                # Located at C:\Users\ahmad\.dbt\profiles.yml

| `STG_WORLDBANK` | RAW_STAGING | Cleaned staging view |├── orchestration/

| `DIM_COUNTRY` | RAW | Country dimension |│   └── dagster/

| `DIM_INDICATOR` | RAW | Indicator dimension |│       └── snowflake_uploader.py   # Dagster pipeline

| `FACT_WORLDBANK` | RAW_MARTS | Analytics fact table |├── data/

│   └── openaq_data.ndjson          # Generated mock data

### dbt Models├── requirements.txt

├── .env                             # Your environment variables

1. **stg_worldbank**: Staging view that filters out null values and standardizes column names└── README.md

2. **dim_country**: Deduplicated country dimension with surrogate keys```

3. **dim_indicator**: Deduplicated indicator dimension with metadata

4. **fact_worldbank**: Main fact table for analysis with all measurements## 🔧 Components



## 🔧 Dagster Pipeline### Snowflake Objects



The Dagster pipeline consists of 4 assets that run in sequence:| Object Type | Name | Purpose |

|------------|------|---------|

1. **fetch_worldbank_data**: Fetches data from World Bank API| Warehouse | `ANALYTICS_WH` | Compute resources (XSMALL, auto-suspend 60s) |

2. **provision_snowflake_objects**: Creates warehouse, database, schemas, and tables| Database | `ANALYTICS_DB` | Container for all schemas and tables |

3. **load_to_snowflake**: Loads data using batch inserts (1000 rows at a time)| Schema | `RAW` | Raw ingestion layer |

4. **run_dbt_models**: Executes dbt transformations| Schema | `RAW_staging` | Staging layer for transformations |

| Schema | `RAW_marts` | Fact and aggregated tables |

## 💻 Usage Examples| Table | `OPENAQ_STREAM` | Raw air quality measurements |



### Query the Data in Snowflake### dbt Models



```sql1. **`stg_openaq.sql`** (Staging)

-- View all countries   - Standardizes raw data from `OPENAQ_STREAM` table

SELECT * FROM ANALYTICS_DB.RAW.DIM_COUNTRY;   - Creates view in `RAW_staging` schema

   - All columns use quoted identifiers for case sensitivity

-- View all indicators

SELECT * FROM ANALYTICS_DB.RAW.DIM_INDICATOR;2. **`dim_station.sql`** (Dimension)

   - Deduplicates monitoring stations

-- Get GDP trends for Egypt   - Generates `station_id` using `row_number()`

SELECT    - Columns: `station_id`, `station_name`, `city`, `country`, `latitude`, `longitude`

    YEAR,

    VALUE as GDP3. **`dim_parameter.sql`** (Dimension)

FROM ANALYTICS_DB.RAW_MARTS.FACT_WORLDBANK   - Lists unique measurement parameters (PM2.5, NO2, O3, etc.)

WHERE COUNTRY_NAME = 'Egypt'    - Generates `parameter_id` using `row_number()`

  AND INDICATOR_NAME = 'GDP (current US$)'   - Columns: `parameter_id`, `parameter_name`, `unit`

ORDER BY YEAR DESC;

4. **`fact_aq.sql`** (Fact Table)

-- Compare life expectancy across countries in 2023   - Contains all air quality measurements

SELECT    - References staging model

    COUNTRY_NAME,   - Schema: `RAW_marts`

    VALUE as LIFE_EXPECTANCY   - Columns: `measurement_id`, `location`, `city`, `country`, `parameter`, `value`, `unit`, `latitude`, `longitude`, `measured_at`, `fetched_at`

FROM ANALYTICS_DB.RAW_MARTS.FACT_WORLDBANK

WHERE INDICATOR_NAME = 'Life expectancy at birth, total (years)'### Dagster Pipeline

  AND YEAR = 2023

ORDER BY VALUE DESC;Located in `orchestration/dagster/snowflake_uploader.py`:

```

- **Job**: `openaq_snowflake_pipeline`

## 🐛 Troubleshooting- **Ops**:

  - `check_raw_data` - Verifies NDJSON file exists

### Dagster won't start  - `stage_openaq_file` - Stages file for Snowflake (PUT command)

  - `upload_openaq_to_snowflake` - Copies staged data into table

Make sure the password is set in your `.env` file and run:  - `verify_upload` - Confirms row count matches



```bash## 📊 Data Schema

dagster dev -f orchestration/dagster/worldbank_pipeline.py

```The `OPENAQ_STREAM` table contains the following columns:



### dbt errors about column names| Column | Type | Description |

|--------|------|-------------|

Snowflake column names are case-sensitive. All column references in dbt models use UPPERCASE (e.g., `COUNTRY_ID`, `YEAR`, `VALUE`).| `measurement_id` | NUMBER | Unique measurement identifier |

| `location` | VARCHAR | Station location name |

### Snowflake connection issues| `city` | VARCHAR | City name |

| `country` | VARCHAR | Country code |

Verify your `.env` file has the correct:| `parameter` | VARCHAR | Pollutant type (PM2.5, NO2, O3, etc.) |

| `value` | FLOAT | Measurement value |

- Account identifier (format: `account.region`)| `unit` | VARCHAR | Unit of measurement (µg/m³, ppm) |

- Username and password| `latitude` | FLOAT | Station latitude |

- Role with sufficient permissions| `longitude` | FLOAT | Station longitude |

| `measured_at` | TIMESTAMP_NTZ | Measurement timestamp |

### Python package errors| `fetched_at` | TIMESTAMP_NTZ | Data retrieval timestamp |



Make sure you're using the correct virtual environment:## 💻 Usage



```bash### Manual Step-by-Step Execution

# Activate venv

venv\Scripts\activate  # Windows```bash

# source venv/bin/activate  # macOS/Linux# 1. Provision Snowflake objects

python scripts/provision_snowflake.py

# Reinstall packages if needed

pip install -r requirements.txt# 2. Generate mock data

```python scripts/generate_mock_openaq.py



## 🔑 Environment Variables# 3. Upload data to Snowflake

python scripts/upload_mock_data.py

| Variable | Description | Example |

|----------|-------------|---------|# 4. Run dbt transformations

| `SNOWFLAKE_ACCOUNT` | Account identifier | `POKMPXO-ICB41863` |cd dbt

| `SNOWFLAKE_USER` | Username | `AHMEDEHAB` |dbt run

| `SNOWFLAKE_PASSWORD` | Password | `your_secure_password` |dbt test

| `SNOWFLAKE_ROLE` | Role | `ACCOUNTADMIN` |```

| `SNOWFLAKE_WAREHOUSE` | Warehouse name | `ANALYTICS_WH` |

| `SNOWFLAKE_DATABASE` | Database name | `ANALYTICS_DB` |### Automated Execution

| `SNOWFLAKE_SCHEMA` | Default schema | `RAW` |

```bash

## 📈 Next Steps# Run entire pipeline with one command

python scripts/run_full_pipeline.py

- **Add Scheduling**: Use Dagster sensors or schedules to run the pipeline automatically```

- **Add More Indicators**: Extend the indicator list in the notebook

- **Create Visualizations**: Connect Power BI or Tableau to Snowflake for dashboards### Query Transformed Data

- **Add Data Quality Checks**: Implement custom dbt tests for business rules

- **Add CI/CD**: Set up GitHub Actions to test dbt models on each commitConnect to Snowflake and run:



## 🤝 Contributing```sql

-- View all air quality measurements

Contributions are welcome! Please:SELECT * FROM ANALYTICS_DB.RAW_marts.FACT_AQ LIMIT 10;



1. Fork the repository-- View stations

2. Create a feature branchSELECT * FROM ANALYTICS_DB.RAW.DIM_STATION;

3. Make your changes

4. Test thoroughly (run dbt and Dagster)-- View parameters

5. Submit a pull requestSELECT * FROM ANALYTICS_DB.RAW.DIM_PARAMETER;



## 📝 License-- Average PM2.5 by city

SELECT 

This project is for educational purposes.    "city",

    AVG("value") as avg_pm25

## 🙏 AcknowledgmentsFROM ANALYTICS_DB.RAW_marts.FACT_AQ

WHERE "parameter" = 'pm25'

- **World Bank Open Data** for providing free development indicatorsGROUP BY "city"

- **Snowflake** for cloud data warehousingORDER BY avg_pm25 DESC;

- **dbt** for SQL-based transformations```

- **Dagster** for modern data orchestration

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
