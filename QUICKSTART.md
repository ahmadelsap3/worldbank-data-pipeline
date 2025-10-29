# Quick Reference Card

## 🚀 One-Command Setup

```bash
# Clone and setup (run once)
git clone https://github.com/ahmadelsap3/air-quality-etl-pipeline.git
cd air-quality-etl-pipeline
python -m venv venv
source venv/bin/activate  # or: .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
```

## ⚙️ Configuration (First Time)

1. **Create `.env` file**:
   ```bash
   cp .env.example .env
   # Edit .env with your Snowflake credentials
   ```

2. **Configure dbt** (see SETUP.md for details):
   ```bash
   # Create ~/.dbt/profiles.yml with your Snowflake credentials
   ```

## ▶️ Run the Pipeline

```bash
# Activate virtual environment first
source venv/bin/activate  # or: .\venv\Scripts\Activate.ps1

# Run complete pipeline
python scripts/run_full_pipeline.py
```

## 🔧 Individual Commands

```bash
# Provision Snowflake objects
python scripts/provision_snowflake.py

# Generate mock data (100 records)
python scripts/generate_mock_openaq.py --records 100

# Upload to Snowflake
python scripts/upload_mock_data.py

# Run dbt transformations
cd dbt
dbt run
dbt test
```

## 📊 Query Examples

```sql
-- View all air quality data
SELECT * FROM ANALYTICS_DB.RAW_marts.FACT_AQ LIMIT 10;

-- View stations
SELECT * FROM ANALYTICS_DB.RAW.DIM_STATION;

-- Average PM2.5 by city
SELECT "city", AVG("value") as avg_pm25
FROM ANALYTICS_DB.RAW_marts.FACT_AQ
WHERE "parameter" = 'pm25'
GROUP BY "city"
ORDER BY avg_pm25 DESC;
```

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| `python: command not found` | Use `py` on Windows, or install Python |
| Scripts disabled (PowerShell) | Run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Snowflake connection fails | Check `.env` credentials and account format |
| dbt errors | Run `cd dbt && dbt debug` to check configuration |
| Module not found | Ensure venv is activated, run `pip install -r requirements.txt` |

## 📖 Full Documentation

- **Setup Guide**: See `SETUP.md` for detailed setup instructions
- **Project Documentation**: See `README.md` for architecture and features
- **Troubleshooting**: Both files have comprehensive troubleshooting sections

## 🔑 Environment Variables

Required in `.env` file:
```
SNOWFLAKE_ACCOUNT=YOUR_ACCOUNT_ID
SNOWFLAKE_USER=YOUR_USERNAME
SNOWFLAKE_PASSWORD=YOUR_PASSWORD
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=ANALYTICS_WH
SNOWFLAKE_DATABASE=ANALYTICS_DB
SNOWFLAKE_SCHEMA=RAW
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `scripts/run_full_pipeline.py` | Master automation script |
| `scripts/provision_snowflake.py` | Creates Snowflake objects |
| `dbt/models/` | Data transformation models |
| `.env` | Your credentials (create from `.env.example`) |
| `~/.dbt/profiles.yml` | dbt Snowflake configuration |

## ✅ Verify Setup

```bash
# Test Python
python --version

# Test dependencies
pip list | grep snowflake
pip list | grep dbt

# Test Snowflake connection
cd dbt
dbt debug

# Test full pipeline
python scripts/run_full_pipeline.py
```

Expected result: `PASS=4 WARN=0 ERROR=0 SKIP=0 TOTAL=4`

## 🎯 Next Steps

1. ✅ Complete setup (see SETUP.md)
2. ✅ Run pipeline successfully
3. ✅ Query data in Snowflake
4. ✅ Connect Power BI (see README.md)
5. ✅ Explore and extend the models
