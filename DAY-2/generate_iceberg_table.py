
# Usage:
# pip install --user pyiceberg[pyarrow,gcsfs] pandas sqlalchemy
#   python3 generate_iceberg_table.py gs://YOUR_BUCKET/iceberg_warehouse

#CREATE OR REPLACE EXTERNAL TABLE `partition_demo.orders_iceberg_biglake`
# WITH CONNECTION `your-project.US.gcs_biglake_conn`
# OPTIONS (
#  format = 'ICEBERG',
#  uris = [
#  'gs://your-bucket/iceberg_warehouse/orders_ns/orders_iceberg/metadata/00001-<uuid>.metadata.json'
#  ]
# );


import sys
import pandas as pd
import pyarrow as pa
from pyiceberg.catalog.sql import SqlCatalog

if len(sys.argv) != 2 or not sys.argv[1].startswith("gs://"):
    print("Usage: python3 generate_iceberg_table.py gs://himanshugcpproject1bucket/iceberg_warehouse")
    sys.exit(1)

warehouse_uri = sys.argv[1].rstrip("/")


catalog = SqlCatalog(
    "demo",
    **{
        "uri": "sqlite:///iceberg_catalog.db",
        "warehouse": warehouse_uri,
    },
)

# Re-use the same orders_sample.csv used throughout the course.
df = pd.read_csv("orders_sample.csv", parse_dates=["order_date", "order_ts"])
table_data = pa.Table.from_pandas(df, preserve_index=False)

catalog.create_namespace_if_not_exists("orders_ns")
if catalog.table_exists("orders_ns.orders_iceberg"):
    catalog.drop_table("orders_ns.orders_iceberg")

iceberg_table = catalog.create_table("orders_ns.orders_iceberg", schema=table_data.schema)
iceberg_table.append(table_data)

print("Iceberg table created.")
print("metadata_location:", iceberg_table.metadata_location)
print()
print("Use that metadata_location as the `uris` value when creating the BigQuery")
print("external table for Iceberg -- see the walkthrough PDF, Step 3.")
