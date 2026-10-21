from banking_dq.dq_run import run_dq
from banking_dq.extract import read_raw
from banking_dq.db import get_engine
from banking_dq.load import load_exceptions, load_table, run_sql_file
from banking_dq.rule_catalog import RULES


# Initialize business date and read raw data
business_date = "20260927"
accounts_df = read_raw("accounts", business_date)
customers_df = read_raw("customers", business_date)
transactions_df = read_raw("transactions", business_date)
fx_df = read_raw("fx_rates", business_date)

# Load data to staging database
engine = get_engine()
load_table(accounts_df, "accounts", engine)
load_table(customers_df, "customers", engine)
load_table(transactions_df, "transactions", engine)
load_table(fx_df, "fx_rates", engine)

# Run data quality checks
all_exceptions_df = run_dq(customers_df, accounts_df, transactions_df, business_date)

# Load the exceptions DataFrame to the database
load_exceptions(all_exceptions_df, engine, business_date)
load_table(RULES, "rule_catalog", engine, schema="dq") 

# Run the SQL file to generate the scorecard view
run_sql_file("sql/scorecard.sql", engine)