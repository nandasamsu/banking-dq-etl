from banking_dq.extract import read_raw
import pandas as pd

df = read_raw("customers", "20260927", base_path="s3://nandasamsu-banking-dq/raw")
print(len(df))
print(df[["source_file", "source_row", "customer_id"]].head(3))