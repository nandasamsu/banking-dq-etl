

from banking_dq.dq_run import run_dq
from banking_dq.extract import read_raw
from banking_dq.rule_catalog import RULES
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--business_date", required =True)
args, _ = parser.parse_known_args()
business_date = args.business_date

bucket_path = "s3://nandasamsu-banking-dq"
customers_df = read_raw("customers", business_date, base_path=f"{bucket_path}/raw")
accounts_df = read_raw("accounts", business_date, base_path=f"{bucket_path}/raw")
transactions_df = read_raw("transactions", business_date, base_path=f"{bucket_path}/raw")
print(f"Read {len(customers_df)} rows from customers, {len(accounts_df)} rows from accounts, and {len(transactions_df)} rows from transactions.")

# Run data quality checks
exceptions_df = run_dq(customers_df, accounts_df, transactions_df, business_date)

# Drop the business_date column before saving to S3 since it's already included in the S3 path
exceptions_df = exceptions_df.drop(columns="business_date")

# Upload the exceptions DataFrame to S3 in Parquet format
exceptions_df.to_parquet(f"{bucket_path}/curated/dq_exception/business_date={business_date}/exceptions.parquet", index=False)
print(f"Uploaded {len(exceptions_df)} rows of exceptions to S3 at {bucket_path}/curated/dq_exception/business_date={business_date}/exceptions.parquet.")

# Upload the rule catalog to S3 in Parquet format
RULES.to_parquet(f"{bucket_path}/curated/rule_catalog/rule_catalog.parquet", index=False)
print(f"Uploaded rule catalog with {len(RULES)} rules to S3 at {bucket_path}/curated/rule_catalog/rule_catalog.parquet.")