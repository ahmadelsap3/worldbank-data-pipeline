# Setup Instructions

Follow these steps to run the World Bank Data Pipeline on your local machine.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.13+** (or Python 3.9+)
- **Git** installed
- **Snowflake Account** with:
  - Account identifier (e.g., `POKMPXO-ICB41863`)
  - Username and password
  - ACCOUNTADMIN role or equivalent permissions

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ahmadelsap3/worldbank-data-pipeline.git
cd worldbank-data-pipeline
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- pandas (data manipulation)
- requests (API calls)
- snowflake-connector-python (Snowflake connection)
- dbt-core and dbt-snowflake (data transformations)
- dagster and dagster-webserver (orchestration)
- jupyter (interactive notebooks)

### 4. Configure Environment Variables

Create a `.env` file in the project root by copying the example:

```bash
# On Windows:
copy .env.example .env

# On macOS/Linux:
cp .env.example .env
```

Edit the `.env` file and add your Snowflake credentials:

```env
SNOWFLAKE_ACCOUNT=your_account.region
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=ANALYTICS_WH
SNOWFLAKE_DATABASE=ANALYTICS_DB
SNOWFLAKE_SCHEMA=RAW
```

**Important:** 
- Replace `your_account.region` with your Snowflake account identifier
- Replace `your_username` and `your_password` with your credentials
- The `.env` file is already in `.gitignore` and will NOT be committed to Git

### 5. Run the Pipeline

You have two options to run the pipeline:

#### Option A: Interactive Jupyter Notebook (Recommended for first run)

```bash
jupyter notebook notebooks/worldbank_data_pipeline.ipynb
```

This will:
1. Open Jupyter in your browser
2. Allow you to run cells step-by-step
3. Fetch World Bank data (7 countries, 7 indicators, 2010-2023)
4. Load ~600+ records into Snowflake

**Execute all cells in order** by clicking "Cell" → "Run All" or using Shift+Enter on each cell.

#### Option B: Automated with Dagster

```bash
dagster dev -f orchestration/dagster/worldbank_pipeline.py
```

This will:
1. Start Dagster web UI at http://localhost:3000
2. Open the URL in your browser
3. Navigate to "Assets" tab
4. Click "Materialize all" to run the complete pipeline

The Dagster pipeline will:
- Fetch data from World Bank API
- Provision Snowflake objects (warehouse, database, schemas, tables)
- Load data to Snowflake
- Run dbt transformations

### 6. Run dbt Transformations (if using Option A)

If you used the Jupyter notebook, run dbt separately:

```bash
cd dbt
dbt run
dbt test
```

This creates:
- **Staging view**: `STG_WORLDBANK` in `RAW_STAGING` schema
- **Dimension tables**: `DIM_COUNTRY`, `DIM_INDICATOR` in `RAW` schema
- **Fact table**: `FACT_WORLDBANK` in `RAW_MARTS` schema

Expected output:
- `dbt run`: 4 models created (PASS=4)
- `dbt test`: 21 tests passed (PASS=21)

### 7. Verify the Pipeline

Connect to Snowflake and run these queries to verify:

```sql
-- Check raw data
SELECT COUNT(*) FROM ANALYTICS_DB.RAW.WORLDBANK_INDICATORS;
-- Expected: ~600+ rows

-- Check staging view
SELECT COUNT(*) FROM ANALYTICS_DB.RAW_STAGING.STG_WORLDBANK;
-- Expected: ~600+ rows (same as raw, but cleaned)

-- Check dimensions
SELECT COUNT(*) FROM ANALYTICS_DB.RAW.DIM_COUNTRY;
-- Expected: 7 rows

SELECT COUNT(*) FROM ANALYTICS_DB.RAW.DIM_INDICATOR;
-- Expected: 7 rows

-- Check fact table
SELECT COUNT(*) FROM ANALYTICS_DB.RAW_MARTS.FACT_WORLDBANK;
-- Expected: ~600+ rows

-- View sample data
SELECT 
    COUNTRY_NAME,
    INDICATOR_NAME,
    YEAR,
    VALUE
FROM ANALYTICS_DB.RAW_MARTS.FACT_WORLDBANK
LIMIT 10;
```

## Troubleshooting

### Issue: Cannot connect to Snowflake

**Solution:**
- Verify your `.env` file has correct credentials
- Check your Snowflake account is active
- Ensure your user has ACCOUNTADMIN role or CREATE permissions
- Test connection with:
  ```python
  import snowflake.connector
  conn = snowflake.connector.connect(
      account='your_account',
      user='your_username',
      password='your_password'
  )
  print("✅ Connected!")
  ```

### Issue: dbt command not found

**Solution:**
- Make sure virtual environment is activated: `venv\Scripts\activate`
- Reinstall dbt: `pip install dbt-core dbt-snowflake`
- Check installation: `dbt --version`

### Issue: Module not found errors

**Solution:**
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall all packages: `pip install -r requirements.txt`

### Issue: dbt profile not found

**Solution:**
- The `dbt/profiles.yml` file should be in the `dbt/` folder
- dbt will read the password from your `.env` file automatically
- If issues persist, run: `dbt debug` to check configuration

### Issue: Dagster aborts immediately

**Solution:**
- Make sure `.env` file exists and has your password
- Try running in a new terminal window
- Check if port 3000 is already in use: `netstat -ano | findstr :3000`
- If occupied, kill the process or use a different port: `dagster dev -f orchestration/dagster/worldbank_pipeline.py -p 3001`

### Issue: No data in Snowflake tables

**Solution:**
- Rerun the Jupyter notebook or Dagster pipeline
- Check the notebook output for errors
- Verify API connection: World Bank API might be slow or temporarily unavailable
- Try reducing the year range if needed

## What Gets Created

After running the full pipeline, you'll have:

### Snowflake Objects

| Object | Type | Location | Purpose |
|--------|------|----------|---------|
| ANALYTICS_WH | Warehouse | - | Compute resources |
| ANALYTICS_DB | Database | - | Container for all data |
| RAW | Schema | ANALYTICS_DB | Raw data tables |
| RAW_STAGING | Schema | ANALYTICS_DB | Staging views |
| RAW_MARTS | Schema | ANALYTICS_DB | Analytics fact tables |
| WORLDBANK_INDICATORS | Table | RAW | Raw API data (~600+ rows) |
| STG_WORLDBANK | View | RAW_STAGING | Cleaned staging data |
| DIM_COUNTRY | Table | RAW | Country dimension (7 rows) |
| DIM_INDICATOR | Table | RAW | Indicator dimension (7 rows) |
| FACT_WORLDBANK | Table | RAW_MARTS | Analytics fact table (~600+ rows) |

### Data Fetched

- **Countries**: Egypt, Saudi Arabia, UAE, Jordan, Nigeria, South Africa, Kenya
- **Indicators**:
  1. Population, total
  2. GDP (current US$)
  3. Life expectancy at birth, total (years)
  4. Mortality rate, infant (per 1,000 live births)
  5. Literacy rate, adult total (% of people ages 15 and above)
  6. CO2 emissions (metric tons per capita)
  7. Access to electricity (% of population)
- **Time Range**: 2010-2023
- **Total Records**: ~600+ (varies based on data availability)

## Next Steps

Once the pipeline is running successfully:

1. **Explore the data** using SQL queries in Snowflake
2. **Modify indicators** by editing the notebook to fetch different World Bank indicators
3. **Add more countries** by expanding the country list
4. **Create visualizations** by connecting Power BI or Tableau to Snowflake
5. **Schedule automated runs** using Dagster schedules or sensors
6. **Add custom dbt tests** for data quality validation

## Need Help?

If you encounter issues not covered here:

1. Check the main [README.md](README.md) for architecture details
2. Review dbt model files in `dbt/models/` to understand transformations
3. Check Dagster pipeline code in `orchestration/dagster/worldbank_pipeline.py`
4. Ensure all environment variables are correctly set in `.env`

## Summary Checklist

- [ ] Python 3.9+ installed
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with Snowflake credentials
- [ ] Jupyter notebook executed OR Dagster pipeline materialized
- [ ] dbt transformations run successfully
- [ ] Data verified in Snowflake
- [ ] ~600+ rows in FACT_WORLDBANK table

✅ **Pipeline is ready!** You can now query and analyze World Bank data in Snowflake.
