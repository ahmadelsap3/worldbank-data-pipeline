"""Quick script to upload mock GTFS transit data to Snowflake"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from orchestration.dagster.snowflake_uploader import upload_ndjson_to_table

ndjson_file = 'data/gtfs_data.ndjson'
table = 'ANALYTICS_DB.RAW.GTFS_TRIPS'

print(f'Uploading {ndjson_file} to {table}...')
rows = upload_ndjson_to_table(ndjson_file, table)
print(f'✓ Uploaded {rows} rows to {table}')
