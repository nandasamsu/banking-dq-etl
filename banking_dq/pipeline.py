import pandas as pd
from banking_dq.mappings import currency_mapping, status_mapping, country_mapping, transaction_type_mapping
from banking_dq.standardize import standardize_value
from banking_dq.extract import read_raw
from banking_dq.db import get_engine
from banking_dq.load import load_exceptions, load_table, run_sql_file
from banking_dq.dq_rules import check_accounts, check_customer, check_transactions
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

# Standardize values in the DataFrames
accounts_df['currency'] = standardize_value(accounts_df['currency'], currency_mapping)
accounts_df['status'] = standardize_value(accounts_df['status'], status_mapping)
customers_df['country'] = standardize_value(customers_df['country'], country_mapping)
transactions_df['transaction_type'] = standardize_value(transactions_df['transaction_type'], transaction_type_mapping) 
transactions_df["currency"] = standardize_value(transactions_df["currency"], currency_mapping)
accounts_df["account_type"] = standardize_value(accounts_df["account_type"], {})

# Perform data quality checks on the customers DataFrame
customer_exceptions_df = check_customer(customers_df, business_date)
account_exceptions_df = check_accounts(accounts_df, business_date, customers_df)
transaction_exceptions_df = check_transactions(transactions_df, business_date, accounts_df)

# Combine all exceptions into a single DataFrame and join them with the RULES DataFrame
all_exceptions_df = pd.concat([customer_exceptions_df, account_exceptions_df, transaction_exceptions_df], ignore_index=True,)
all_exceptions_df["business_date"] = business_date
all_exceptions_df = all_exceptions_df.merge(RULES, on="rule_id", how="left")

# Load the exceptions DataFrame to the database
load_exceptions(all_exceptions_df, engine, business_date)
load_table(RULES, "rule_catalog", engine, schema="dq") 

# Run the SQL file to generate the scorecard view
run_sql_file("sql/scorecard.sql", engine)