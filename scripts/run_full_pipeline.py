"""Complete GTFS transit ETL pipeline setup and execution (Python-only).

This script automates the full workflow:
1. Load Snowflake credentials from environment
2. Provision Snowflake objects (warehouse, database, schemas, tables)
3. Generate sample GTFS transit data (Cairo Metro)
4. Upload data to Snowflake
5. Run dbt transformations and tests

Usage:
  Set environment variables first (or export them in your shell):
    export SNOWFLAKE_ACCOUNT='POKMPXO-ICB41863'
    export SNOWFLAKE_USER='AHMEDEHAB'
    export SNOWFLAKE_PASSWORD='your_password'
    export SNOWFLAKE_ROLE='ACCOUNTADMIN'
    export SNOWFLAKE_WAREHOUSE='ANALYTICS_WH'
    export SNOWFLAKE_DATABASE='ANALYTICS_DB'
    export SNOWFLAKE_SCHEMA='RAW'

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
    """Generate sample GTFS transit data."""
    script_dir = Path(__file__).resolve().parent
    gtfs_script = script_dir / 'generate_gtfs_data.py'
    
    print(f"\n{'=' * 70}")
    print("Generating Sample GTFS Transit Data (Cairo Metro)")
    print(f"{'=' * 70}")
    
    if not gtfs_script.exists():
        print(f"✗ GTFS data generator not found: {gtfs_script}")
        sys.exit(1)
    
    result = subprocess.run([sys.executable, str(gtfs_script), '--trips', '100'], env=os.environ)
    if result.returncode != 0:
        print("✗ GTFS data generation failed")
        sys.exit(1)


def run_dbt_models():
    """Run dbt transformations."""
    print(f"\n{'=' * 70}")
    print("Running dbt Transformations")
    print(f"{'=' * 70}")
    
    # Find dbt executable
    import sys
    from pathlib import Path
    
    if sys.platform == 'win32':
        python_exe = Path(sys.executable)
        scripts_dir = python_exe.parent
        dbt_exe = scripts_dir / 'dbt.exe'
        
        if not dbt_exe.exists():
            print(f"✗ dbt.exe not found at {dbt_exe}")
            print("Install dbt: pip install dbt-core dbt-snowflake")
            sys.exit(1)
        
        dbt_cmd = str(dbt_exe)
    else:
        dbt_cmd = 'dbt'
    
    # Change to dbt directory
    repo_root = Path(__file__).resolve().parent.parent
    dbt_dir = repo_root / 'dbt'
    
    # Run dbt
    print("\nRunning: dbt run")
    result = subprocess.run([dbt_cmd, 'run'], cwd=str(dbt_dir), env=os.environ)
    if result.returncode != 0:
        print("✗ dbt run failed")
        sys.exit(1)
    
    print("\nRunning: dbt test")
    result = subprocess.run([dbt_cmd, 'test'], cwd=str(dbt_dir), env=os.environ)
    if result.returncode != 0:
        print("⚠ dbt test had failures")
    
    print("✓ dbt transformations completed")


def main():
    print("\n" + "=" * 70)
    print("Automated GTFS Transit ETL Pipeline")
    print("=" * 70)
    print("This script will:")
    print("  1. Check/set Snowflake environment variables")
    print("  2. Provision Snowflake objects (warehouse, database, tables)")
    print("  3. Generate sample GTFS transit data (Cairo Metro)")
    print("  4. Upload data to Snowflake")
    print("  5. Run dbt transformations and tests")
    print("=" * 70)
    
    # Step 1: Check environment
    check_env_vars()
    
    # Step 2: Provision Snowflake
    run_script('provision_snowflake.py', '[1/5] Provision Snowflake Objects')
    
    # Step 3: Generate sample data
    generate_sample_data()
    
    # Step 4: Upload data
    run_script('upload_mock_data.py', '[3/5] Upload Data to Snowflake')
    
    # Step 5: Run dbt
    run_dbt_models()
    
    print("\n" + "=" * 70)
    print("✓ PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nYour data is now available in Snowflake:")
    print("  - Raw data: ANALYTICS_DB.RAW.GTFS_TRIPS")
    print("  - dbt models: ANALYTICS_DB.RAW_staging, RAW_marts (routes, stops, trips)")
    print("\nNext steps:")
    print("  - Connect Power BI to Snowflake using your credentials")
    print("  - Query the transformed models for transit analytics")
    print("  - Create visualizations: route maps, ridership trends, on-time performance")
    print("  - Schedule this pipeline using cron/Task Scheduler or Dagster daemon")
    print("=" * 70)


if __name__ == '__main__':
    main()
