# Setup Guide for New Contributors

Welcome! This guide will help you set up the air quality ETL pipeline on your local machine.

## 📋 Prerequisites

Before starting, ensure you have:

1. **Python 3.9+** (3.13 recommended)
   - Download from: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Git**
   - Download from: https://git-scm.com/downloads
   - Verify: `git --version`

3. **Snowflake Account**
   - You'll need account credentials (contact project admin)
   - Account ID, username, password, role

4. **Power BI Desktop** (Optional - for visualization)
   - Download from: https://powerbi.microsoft.com/desktop/

## 🚀 Quick Start (5 Steps)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ahmadelsap3/air-quality-etl-pipeline.git
cd air-quality-etl-pipeline
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Troubleshooting**: If PowerShell script execution is blocked:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- `snowflake-connector-python` - Snowflake database connector
- `dbt-core` and `dbt-snowflake` - Data transformation framework
- `dagster` and `dagster-webserver` - Orchestration platform
- `python-dotenv` - Environment variable management

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your Snowflake credentials:

```env
# Snowflake Configuration
SNOWFLAKE_ACCOUNT=YOUR_ACCOUNT_ID       # e.g., POKMPXO-ICB41863
SNOWFLAKE_USER=YOUR_USERNAME            # e.g., AHMEDEHAB
SNOWFLAKE_PASSWORD=YOUR_PASSWORD        # Your Snowflake password
SNOWFLAKE_ROLE=ACCOUNTADMIN            # Or your assigned role
SNOWFLAKE_WAREHOUSE=ANALYTICS_WH       # Will be created by provisioning script
SNOWFLAKE_DATABASE=ANALYTICS_DB        # Will be created by provisioning script
SNOWFLAKE_SCHEMA=RAW                   # Default schema

# Optional: OpenAQ API (if using real data instead of mock)
# OPENAQ_API_KEY=your_api_key_here
```

**Important**: Never commit the `.env` file to Git (it's already in `.gitignore`)

### Step 5: Configure dbt Profile

The pipeline uses dbt for data transformations. Configure your profile:

**Windows:**
```powershell
# Create .dbt directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.dbt"

# Create profiles.yml
@"
hotels_egypt_profile:
  outputs:
    dev:
      type: snowflake
      account: YOUR_ACCOUNT_ID
      user: YOUR_USERNAME
      password: YOUR_PASSWORD
      role: ACCOUNTADMIN
      database: ANALYTICS_DB
      warehouse: ANALYTICS_WH
      schema: RAW
      threads: 4
      client_session_keep_alive: False
  target: dev
"@ | Out-File -FilePath "$env:USERPROFILE\.dbt\profiles.yml" -Encoding UTF8
```

**macOS/Linux:**
```bash
mkdir -p ~/.dbt
cat > ~/.dbt/profiles.yml <<EOF
hotels_egypt_profile:
  outputs:
    dev:
      type: snowflake
      account: YOUR_ACCOUNT_ID
      user: YOUR_USERNAME
      password: YOUR_PASSWORD
      role: ACCOUNTADMIN
      database: ANALYTICS_DB
      warehouse: ANALYTICS_WH
      schema: RAW
      threads: 4
      client_session_keep_alive: False
  target: dev
EOF
```

**Replace**: `YOUR_ACCOUNT_ID`, `YOUR_USERNAME`, `YOUR_PASSWORD` with your actual credentials.

## ✅ Verify Installation

### Test Python and Dependencies

```bash
python --version           # Should show 3.9+
pip list | grep snowflake  # Should show snowflake-connector-python
pip list | grep dbt        # Should show dbt-core and dbt-snowflake
```

### Test dbt Configuration

```bash
cd dbt
dbt debug
```

Expected output:
```
Connection test: [OK connection ok]
```

If you see errors, check your `~/.dbt/profiles.yml` configuration.

### Test Snowflake Connection

```bash
python -c "from scripts.provision_snowflake import get_snowflake_connection; conn = get_snowflake_connection(); print('✅ Connection successful')"
```

## 🏃 Run the Pipeline

Once everything is set up, run the complete pipeline:

```bash
python scripts/run_full_pipeline.py
```

This will:
1. ✅ Provision Snowflake warehouse, database, schemas, and tables
2. ✅ Generate 100 mock air quality records
3. ✅ Upload data to Snowflake
4. ✅ Run dbt transformations (4 models)
5. ✅ Verify data quality

Expected output:
```
=== Starting Full Pipeline Execution ===

[1/5] Provisioning Snowflake objects...
✓ Created warehouse ANALYTICS_WH
✓ Created database ANALYTICS_DB
✓ Created schemas: RAW, RAW_staging, RAW_marts
✓ Created table: OPENAQ_STREAM

[2/5] Generating mock data...
✓ Wrote 100 mock measurements to data/openaq_data.ndjson

[3/5] Uploading to Snowflake...
✓ Uploaded 100 rows to ANALYTICS_DB.RAW.OPENAQ_STREAM

[4/5] Running dbt transformations...
1 of 4 OK created sql view model RAW_staging.stg_openaq
2 of 4 OK created sql view model RAW.dim_parameter
3 of 4 OK created sql view model RAW.dim_station
4 of 4 OK created sql view model RAW_marts.fact_aq
Done. PASS=4 WARN=0 ERROR=0 SKIP=0 TOTAL=4

[5/5] Running dbt tests...
Done. PASS=4 WARN=0 ERROR=0 SKIP=0 TOTAL=4

=== Pipeline completed successfully! ===
```

## 📊 Query the Data

After running the pipeline, you can query the transformed data:

```sql
-- Connect to Snowflake and run:

-- View all air quality measurements
SELECT * FROM ANALYTICS_DB.RAW_marts.FACT_AQ LIMIT 10;

-- View monitoring stations
SELECT * FROM ANALYTICS_DB.RAW.DIM_STATION;

-- View measured parameters
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

## 🐛 Common Issues & Solutions

### Issue 1: Python Not Found

**Error**: `python: command not found`

**Solution**:
- Windows: Add Python to PATH during installation, or use `py` instead of `python`
- macOS/Linux: Install Python via package manager (`brew install python3` or `apt install python3`)

### Issue 2: pip Install Fails

**Error**: `pip: command not found` or permission errors

**Solution**:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Use python -m pip instead of pip directly
python -m pip install -r requirements.txt
```

### Issue 3: PowerShell Script Execution Policy

**Error**: `cannot be loaded because running scripts is disabled`

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 4: Snowflake Connection Failed

**Error**: `250001: Could not connect to Snowflake backend`

**Solutions**:
1. Verify account ID format: `ACCOUNT-REGION` (e.g., `POKMPXO-ICB41863`)
2. Check username and password are correct
3. Ensure your IP is not blocked by firewall
4. Verify network connectivity: `ping your_account.snowflakecomputing.com`

### Issue 5: dbt Compilation Errors

**Error**: `invalid identifier 'COLUMN_NAME'`

**Solution**:
- All Snowflake column names must use quoted identifiers: `"column_name"`
- Check your dbt models use quotes consistently
- This project already has proper quoting in all models

### Issue 6: Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'snowflake'`

**Solution**:
1. Ensure virtual environment is activated (you should see `(venv)` in prompt)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Verify installation: `pip list | grep snowflake`

## 📁 Project Structure Overview

```
air-quality-etl-pipeline/
├── scripts/                     # Python automation scripts
│   ├── provision_snowflake.py   # Creates Snowflake objects
│   ├── generate_mock_openaq.py  # Generates test data
│   ├── upload_mock_data.py      # Uploads to Snowflake
│   └── run_full_pipeline.py     # Master automation script
├── dbt/                         # Data transformation models
│   ├── models/
│   │   ├── staging/             # Staging layer
│   │   ├── dimensions/          # Dimension tables
│   │   └── marts/               # Fact tables
│   └── dbt_project.yml          # dbt configuration
├── orchestration/               # Dagster orchestration
│   └── dagster/
│       └── snowflake_uploader.py
├── data/                        # Generated data files
├── .env                         # Your credentials (create this)
├── .env.example                 # Template for .env
├── requirements.txt             # Python dependencies
├── README.md                    # Main documentation
└── SETUP.md                     # This file
```

## 🎓 Learning Resources

### Snowflake
- [Snowflake Getting Started](https://docs.snowflake.com/en/user-guide-getting-started.html)
- [Snowflake SQL Reference](https://docs.snowflake.com/en/sql-reference.html)

### dbt
- [dbt Tutorial](https://docs.getdbt.com/tutorial/learning-more/getting-started-dbt-core)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)

### Dagster
- [Dagster Tutorial](https://docs.dagster.io/tutorial)
- [Dagster Concepts](https://docs.dagster.io/concepts)

## 🤝 Getting Help

If you encounter issues:

1. **Check the main README**: `README.md` has comprehensive troubleshooting
2. **Review logs**: Check `dbt/logs/dbt.log` for dbt errors
3. **Test components individually**:
   ```bash
   # Test Snowflake provisioning
   python scripts/provision_snowflake.py
   
   # Test data generation
   python scripts/generate_mock_openaq.py
   
   # Test dbt models
   cd dbt
   dbt run
   dbt test
   ```
4. **Contact the team**: Open an issue on GitHub or reach out to project maintainers

## 🎯 Next Steps After Setup

1. **Explore the data**: Run queries in Snowflake to understand the schema
2. **Review dbt models**: Check `dbt/models/` to see transformation logic
3. **Connect Power BI**: Follow the Power BI guide in `README.md`
4. **Modify and extend**: Try adding new dbt models or data sources
5. **Run tests**: Execute `dbt test` to ensure data quality

## ✨ You're Ready!

Once you've completed these steps, you should have:
- ✅ Working Python environment with all dependencies
- ✅ Snowflake connection configured
- ✅ dbt profile set up
- ✅ Data loaded and transformed
- ✅ All models tested and passing

Happy coding! 🚀
