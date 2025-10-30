# World Bank Data Pipeline


An automated ETL pipeline that fetches development indicators from the World Bank, loads the data into Snowflake, and runs transformations using dbt. The entire process is orchestrated by Dagster.

## Architecture

```
World Bank API
      ↓
Python ETL (pandas, requests)
      ↓
Snowflake Data Warehouse
  ├── RAW Schema (raw tables)
  ├── RAW_STAGING Schema (staging views)
  └── RAW_MARTS Schema (analytics-ready tables)
      ↓
dbt Transformations
      ↓
Dagster Orchestration
```

## Technology Stack

- **ETL & Orchestration**: Python, Dagster
- **Data Manipulation**: pandas
- **Data Warehouse**: Snowflake
- **Data Transformation**: dbt
- **Interactive Development**: Jupyter Notebook

## Prerequisites

- Python 3.9+
- A Snowflake account with `ACCOUNTADMIN` privileges
- Git

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ahmadelsap3/worldbank-data-pipeline.git
cd worldbank-data-pipeline
```

### 2. Create and Activate Virtual Environment

```bash
# Create the environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Snowflake Credentials

Create a `.env` file by copying the example template. This file will store your credentials securely.

```bash
# On Windows
copy .env.example .env

# On macOS/Linux
cp .env.example .env
```

Now, edit the `.env` file and add your Snowflake account details:

```env
SNOWFLAKE_ACCOUNT=your_account.region
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=ANALYTICS_WH
SNOWFLAKE_DATABASE=ANALYTICS_DB
SNOWFLAKE_SCHEMA=RAW
```
> **Note**: The `.env` file is listed in `.gitignore`, so your credentials will never be committed to the repository.

---

## How to Run the Pipeline

You can run the pipeline using either Jupyter for interactive development or Dagster for automated orchestration.

### Option 1: Jupyter Notebook (Recommended for First Use)

This method is great for understanding the pipeline step-by-step.

```bash
jupyter notebook notebooks/worldbank_data_pipeline.ipynb
```

Inside the notebook, run all cells in order. This will execute the entire ETL process: fetching data, provisioning Snowflake objects, loading data, and running dbt transformations.

### Option 2: Dagster (for Orchestration)

This method is ideal for automated runs and monitoring.

```bash
dagster dev -f orchestration/dagster/worldbank_pipeline.py
```

Open your browser to `http://localhost:3000` and click the **"Materialize all"** button to execute the pipeline.

---

## Data Overview

### Fetched Data

- **Countries**: Egypt, Saudi Arabia, UAE, Jordan, Nigeria, South Africa, Kenya
- **Indicators**: Population, GDP, Life Expectancy, Infant Mortality, Literacy Rate, CO2 Emissions, and Access to Electricity.
- **Time Period**: 2010-2023
- **Total Records**: Approximately 600+

### Snowflake Objects Created

| Object Type | Name | Schema | Description |
|-------------|----------------------|-------------|--------------------------|
| Table | WORLDBANK_INDICATORS | RAW | Raw data from the API |
| View | STG_WORLDBANK | RAW_STAGING | Cleaned staging data |
| Table | DIM_COUNTRY | RAW | Dimension table for countries |
| Table | DIM_INDICATOR | RAW | Dimension table for indicators |
| Table | FACT_WORLDBANK | RAW_MARTS | Final analytics fact table |

---

## SQL Query Examples

After running the pipeline, you can query the transformed data in Snowflake.

### Example 1: GDP Trends for Egypt

```sql
SELECT
    YEAR,
    VALUE as GDP
FROM ANALYTICS_DB.RAW_MARTS.FACT_WORLDBANK
WHERE COUNTRY_NAME = 'Egypt'
  AND INDICATOR_NAME = 'GDP (current US$)'
ORDER BY YEAR DESC;
```

### Example 2: Compare Life Expectancy in 2023

```sql
SELECT
    COUNTRY_NAME,
    VALUE as LIFE_EXPECTANCY
FROM ANALYTICS_DB.RAW_MARTS.FACT_WORLDBANK
WHERE INDICATOR_NAME = 'Life expectancy at birth, total (years)'
  AND YEAR = 2023
ORDER BY VALUE DESC;
```

---

## Troubleshooting

- **Connection Errors**: Double-check your credentials in the `.env` file. Ensure your Snowflake account identifier is in the format `account.region`.
- **dbt Errors**: All column names in the dbt models are `UPPERCASE` to match Snowflake's default case. Run `dbt debug` from within the `dbt/` directory to diagnose issues.
- **Python Errors**: Make sure your virtual environment is activated. If you see `ModuleNotFoundError`, run `pip install -r requirements.txt` again.
- **Dagster UI Not Starting**: The `dagster dev` command requires the `.env` file to be present. Also, ensure port 3000 is free or specify a different one with the `-p` flag (e.g., `-p 3001`).

## License

This project is for educational purposes.
