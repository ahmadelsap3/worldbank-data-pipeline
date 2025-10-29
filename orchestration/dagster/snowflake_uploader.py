"""Small Snowflake uploader scaffold.

This module provides a simple helper to upload newline-delimited JSON (NDJSON)
into a Snowflake table by parsing the file in Python and inserting rows.

Notes:
- This is a scaffold for small-to-moderate files. For large files prefer staging (S3/GCS)
  and COPY INTO in Snowflake.
- Credentials are read from environment variables (see `upload_openaq_to_snowflake`).
"""
from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Iterable, Tuple

try:
    import snowflake.connector
except Exception:  # pragma: no cover - connector may not be installed in test env
    snowflake = None  # type: ignore


DEFAULT_COLUMNS = [
    "measurement_id",
    "location",
    "city",
    "country",
    "parameter",
    "value",
    "unit",
    "latitude",
    "longitude",
    "date_utc",
    "fetched_at",
]


def _read_ndjson_rows(path: Path) -> Iterable[Tuple]:
    with path.open("r", encoding="utf8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            # If the record wraps the feature (e.g., fetched_at + feature), flatten
            if "feature" in obj and isinstance(obj["feature"], dict):
                # Some producers (USGS) used {fetched_at, feature}; OpenAQ writes flat keys
                # Try to extract common keys if present
                feat = obj["feature"]
                props = feat.get("properties", {})
                geom = feat.get("geometry", {})
                yield (
                    obj.get("fetched_at"),
                    props.get("id") or props.get("code"),
                    props.get("place"),
                    geom.get("coordinates", [None, None])[1] if geom else None,
                )
            else:
                # Expect flat record with keys listed in DEFAULT_COLUMNS
                yield tuple(obj.get(c) for c in DEFAULT_COLUMNS)


def upload_ndjson_to_table(
    file_path: str | Path,
    table: str,
    columns: list[str] | None = None,
    batch_size: int = 500,
) -> int:
    """Parse NDJSON and insert rows into Snowflake table.

    Args:
        file_path: path to the NDJSON file
        table: fully qualified table name (e.g. MYDB.PUBLIC.openaq_stream or just schema.table)
        columns: list of column names matching the JSON keys (defaults to DEFAULT_COLUMNS)
        batch_size: how many rows to insert per executemany

    Returns:
        total rows inserted
    """
    if snowflake is None:
        raise RuntimeError("snowflake-connector-python is not installed")

    cols = columns or DEFAULT_COLUMNS
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(str(path))

    # Read credentials from environment
    conn_kwargs = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    }
    missing = [k for k, v in conn_kwargs.items() if k in ("account", "user", "password") and not v]
    if missing:
        raise RuntimeError(f"Missing Snowflake credentials in environment: {missing}")

    # Connect and insert
    con = snowflake.connector.connect(
        account=conn_kwargs["account"],
        user=conn_kwargs["user"],
        password=conn_kwargs["password"],
        role=conn_kwargs.get("role"),
        warehouse=conn_kwargs.get("warehouse"),
        database=conn_kwargs.get("database"),
        schema=conn_kwargs.get("schema"),
    )
    cur = con.cursor()
    try:
        placeholders = ",".join(["%s"] * len(cols))
        # Quote column names to preserve case in Snowflake
        col_list = ",".join([f'"{c}"' for c in cols])
        insert_sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"

        total = 0
        batch = []
        for row in _read_ndjson_rows(path):
            # ensure row has same length
            if len(row) != len(cols):
                # try to align by truncating or padding
                row = tuple(list(row)[: len(cols)] + [None] * max(0, len(cols) - len(row)))
            batch.append(row)
            if len(batch) >= batch_size:
                cur.executemany(insert_sql, batch)
                con.commit()
                total += len(batch)
                batch = []
        if batch:
            cur.executemany(insert_sql, batch)
            con.commit()
            total += len(batch)
        return total
    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            con.close()
        except Exception:
            pass


def create_table_if_not_exists(table: str, columns: list[Tuple[str, str]] | None = None) -> None:
    """Create a Snowflake table if it does not exist.

    Args:
        table: fully qualified table name (e.g. MYDB.PUBLIC.MYTABLE or schema.table)
        columns: list of (name, type) tuples. If None, a sensible default is used.
    """
    if snowflake is None:
        raise RuntimeError("snowflake-connector-python is not installed")

    conn_kwargs = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    }
    missing = [k for k, v in conn_kwargs.items() if k in ("account", "user", "password") and not v]
    if missing:
        raise RuntimeError(f"Missing Snowflake credentials in environment: {missing}")

    # Default column types for OpenAQ
    if columns is None:
        columns = [
            ("measurement_id", "VARCHAR"),
            ("location", "VARCHAR"),
            ("city", "VARCHAR"),
            ("country", "VARCHAR"),
            ("parameter", "VARCHAR"),
            ("value", "FLOAT"),
            ("unit", "VARCHAR"),
            ("latitude", "FLOAT"),
            ("longitude", "FLOAT"),
            ("date_utc", "TIMESTAMP_LTZ"),
            ("fetched_at", "TIMESTAMP_LTZ"),
        ]

    con = snowflake.connector.connect(
        account=conn_kwargs["account"],
        user=conn_kwargs["user"],
        password=conn_kwargs["password"],
        role=conn_kwargs.get("role"),
        warehouse=conn_kwargs.get("warehouse"),
        database=conn_kwargs.get("database"),
        schema=conn_kwargs.get("schema"),
    )
    cur = con.cursor()
    try:
        cols_sql = ", \n    ".join([f'"{name}" {typ}' for name, typ in columns])
        ddl = f"CREATE TABLE IF NOT EXISTS {table} (\n    {cols_sql}\n)"
        cur.execute(ddl)
        con.commit()
    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            con.close()
        except Exception:
            pass
