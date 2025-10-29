"""Complete ETL pipeline setup and execution (Python-only).

This script automates the full workflow:
1. Load Snowflake credentials from environment
2. Provision Snowflake objects (warehouse, database, schemas, tables)
3. Generate sample OpenAQ data
4. Run the Dagster pipeline (upload + dbt + tests)

Usage:
  Set environment variables first (or export them in your shell):
    export SNOWFLAKE_ACCOUNT='POKMPXO-ICB41863'
    export SNOWFLAKE_USER='AHMEDEHAB'
    export SNOWFLAKE_PASSWORD='your_password'
    export SNOWFLAKE_ROLE='ACCOUNTADMIN'
    export SNOWFLAKE_WAREHOUSE='ANALYTICS_WH'
    export SNOWFLAKE_DATABASE='ANALYTICS_DB'
    export SNOWFLAKE_SCHEMA='RAW'
    export SNOWFLAKE_TARGET_TABLE='ANALYTICS_DB.RAW.OPENAQ_STREAM'

  Then run:
    python scripts/run_full_pipeline.py
"""
import os
import sys
import time
import subprocess
import getpass
from pathlib import Path


def check_env_vars():
    """Check and prompt for required environment variables."""
    required = {
        'SNOWFLAKE_ACCOUNT': 'POKMPXO-ICB41863',
        'SNOWFLAKE_USER': 'AHMEDEHAB',
        'SNOWFLAKE_ROLE': 'ACCOUNTADMIN',
        'SNOWFLAKE_WAREHOUSE': 'ANALYTICS_WH',
        'SNOWFLAKE_DATABASE': 'ANALYTICS_DB',
        'SNOWFLAKE_SCHEMA': 'RAW',
        'SNOWFLAKE_TARGET_TABLE': 'ANALYTICS_DB.RAW.OPENAQ_STREAM',
    }
    
    print("=" * 70)
    print("Checking Snowflake Environment Variables")
    print("=" * 70)
    
    for var, default in required.items():
        if not os.getenv(var):
            print(f"Setting {var} = {default}")
            os.environ[var] = default
        else:
            print(f"✓ {var} = {os.getenv(var)}")
    
    # Prompt for password if not set
    if not os.getenv('SNOWFLAKE_PASSWORD'):
        print("\nSNOWFLAKE_PASSWORD not set.")
        password = getpass.getpass("Enter Snowflake password: ")
        os.environ['SNOWFLAKE_PASSWORD'] = password
    else:
        print("✓ SNOWFLAKE_PASSWORD is set")
    
    print()


def run_script(script_name: str, description: str):
    """Run a Python script and check for errors."""
    script_dir = Path(__file__).resolve().parent
    script_path = script_dir / script_name
    
    if not script_path.exists():
        print(f"✗ Script not found: {script_path}")
        sys.exit(1)
    
    print(f"\n{'=' * 70}")
    print(f"{description}")
    print(f"{'=' * 70}")
    
    result = subprocess.run([sys.executable, str(script_path)], env=os.environ)
    
    if result.returncode != 0:
        print(f"\n✗ {description} failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    
    print(f"✓ {description} completed successfully")
    return result.returncode


def generate_sample_data():
    """Generate a small sample of OpenAQ data."""
    script_dir = Path(__file__).resolve().parent
    stream_script = script_dir / 'stream_openaq.py'
    mock_script = script_dir / 'generate_mock_openaq.py'
    
    print(f"\n{'=' * 70}")
    print("Generating Sample OpenAQ Data")
    print(f"{'=' * 70}")
    
    # Try real OpenAQ API first
    if stream_script.exists():
        print("Attempting to fetch real OpenAQ data...")
        proc = subprocess.Popen([sys.executable, str(stream_script), '--interval', '5'], env=os.environ)
        
        try:
            time.sleep(10)
            proc.terminate()
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    
    # Check if real data was created
    ndjson_file = script_dir.parent / 'data' / 'stream' / 'openaq_cairo.ndjson'
    if ndjson_file.exists() and ndjson_file.stat().st_size > 0:
        lines = len(ndjson_file.read_text(encoding='utf-8').strip().split('\n'))
        print(f"✓ Fetched {lines} real OpenAQ records")
        return
    
    # Fall back to mock data if API failed
    print("⚠ OpenAQ API unavailable (authentication required or deprecated)")
    print("Generating mock data for testing...")
    
    if not mock_script.exists():
        print(f"✗ Mock data generator not found: {mock_script}")
        sys.exit(1)
    
    result = subprocess.run([sys.executable, str(mock_script), '--records', '100'], env=os.environ)
    if result.returncode != 0:
        print(f"✗ Mock data generation failed")
        sys.exit(1)


def main():
    print("\n" + "=" * 70)
    print("Automated ETL Pipeline Setup and Execution")
    print("=" * 70)
    print("This script will:")
    print("  1. Check/set Snowflake environment variables")
    print("  2. Provision Snowflake objects (warehouse, database, tables)")
    print("  3. Generate sample OpenAQ data")
    print("  4. Run the Dagster pipeline (upload + dbt + tests)")
    print("=" * 70)
    
    # Step 1: Check environment
    check_env_vars()
    
    # Step 2: Provision Snowflake
    run_script('provision_snowflake.py', 'Step 1/3: Provision Snowflake Objects')
    
    # Step 3: Generate sample data
    generate_sample_data()
    
    # Step 4: Run the pipeline
    run_script('run_pipeline.py', 'Step 3/3: Run Dagster Pipeline')
    
    print("\n" + "=" * 70)
    print("✓ PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nYour data is now available in Snowflake:")
    print("  - Raw data: ANALYTICS_DB.RAW.OPENAQ_STREAM")
    print("  - dbt models: ANALYTICS_DB.MODELS (staging + marts + dimensions)")
    print("\nNext steps:")
    print("  - Connect Power BI to Snowflake using your credentials")
    print("  - Query the models in ANALYTICS_DB.MODELS schema")
    print("  - Schedule this pipeline using cron/Task Scheduler or Dagster daemon")
    print("=" * 70)


if __name__ == '__main__':
    main()
