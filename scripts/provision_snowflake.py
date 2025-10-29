"""Provision Snowflake warehouse, database, schemas, and tables.

This script reads and executes all SQL files from sql/snowflake/ in lexical order,
creating the necessary Snowflake objects for the ETL pipeline.

Requires environment variables:
  SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ROLE (optional)
"""
import os
import sys
from pathlib import Path

try:
    import snowflake.connector
except ImportError:
    print("ERROR: snowflake-connector-python is not installed.")
    print("Run: pip install snowflake-connector-python")
    sys.exit(1)


def get_snowflake_connection():
    """Create a Snowflake connection using environment variables."""
    required = ['SNOWFLAKE_ACCOUNT', 'SNOWFLAKE_USER', 'SNOWFLAKE_PASSWORD']
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        print(f"ERROR: Missing required environment variables: {', '.join(missing)}")
        print("Set them before running this script.")
        sys.exit(1)
    
    conn_kwargs = {
        'account': os.getenv('SNOWFLAKE_ACCOUNT'),
        'user': os.getenv('SNOWFLAKE_USER'),
        'password': os.getenv('SNOWFLAKE_PASSWORD'),
        'role': os.getenv('SNOWFLAKE_ROLE', 'ACCOUNTADMIN'),  # Use ACCOUNTADMIN for provisioning
    }
    
    print(f"Connecting to Snowflake account: {conn_kwargs['account']} as {conn_kwargs['user']}")
    return snowflake.connector.connect(**conn_kwargs)


def execute_sql_file(cursor, connection, sql_file: Path):
    """Execute a SQL file, handling multi-statement files."""
    print(f"\n▶ Executing: {sql_file.name}")
    content = sql_file.read_text(encoding='utf-8')
    
    # Remove comment-only lines first
    lines = []
    for line in content.split('\n'):
        stripped = line.strip()
        # Keep non-comment lines and lines that have code before a comment
        if stripped and not stripped.startswith('--'):
            # Remove inline comments
            if '--' in line:
                line = line[:line.index('--')]
            if line.strip():
                lines.append(line)
    
    clean_content = '\n'.join(lines)
    
    # Split by semicolons and preserve order
    statements = []
    for stmt in clean_content.split(';'):
        stmt = stmt.strip()
        if stmt:
            statements.append(stmt)
    
    for i, stmt in enumerate(statements, 1):
        try:
            # Get first line for preview
            first_line = stmt.split('\n')[0].strip()[:60]
            print(f"  → Executing: {first_line}...")
            
            cursor.execute(stmt)
            connection.commit()  # Commit after each statement to ensure objects exist
            print(f"  ✓ Statement {i} completed")
        except Exception as e:
            print(f"  ✗ Statement {i} failed: {e}")
            print(f"    Full statement:\n{stmt[:300]}...")
            raise


def main():
    # Find the sql/snowflake directory
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    sql_dir = repo_root / 'sql' / 'snowflake'
    
    if not sql_dir.exists():
        print(f"ERROR: SQL directory not found: {sql_dir}")
        sys.exit(1)
    
    # Get all .sql files (excluding the example COPY file)
    sql_files = sorted([f for f in sql_dir.glob('*.sql') if f.name != '05_copy_into_example.sql'])
    
    if not sql_files:
        print(f"ERROR: No SQL files found in {sql_dir}")
        sys.exit(1)
    
    print("=" * 70)
    print("Snowflake Provisioning Script")
    print("=" * 70)
    print(f"Found {len(sql_files)} SQL file(s) to execute:")
    for f in sql_files:
        print(f"  - {f.name}")
    
    # Connect and execute
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    
    try:
        for sql_file in sql_files:
            execute_sql_file(cursor, conn, sql_file)
        
        conn.commit()
        print("\n" + "=" * 70)
        print("✓ Snowflake provisioning completed successfully!")
        print("=" * 70)
        print("\nCreated:")
        print("  - Warehouse: ANALYTICS_WH")
        print("  - Database: ANALYTICS_DB")
        print("  - Schemas: ANALYTICS_DB.RAW, ANALYTICS_DB.MODELS")
        print("  - Table: ANALYTICS_DB.RAW.OPENAQ_STREAM")
        print("  - Role: ANALYTICS_ROLE (with grants)")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Provisioning failed: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()
