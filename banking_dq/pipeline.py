
import pandas as pd
from banking_dq.mappings import currency_mapping, status_mapping, country_mapping, transaction_type_mapping
from banking_dq.standardize import standardize_value

accounts_df = pd.read_csv("data/raw/accounts_20260927.csv", keep_default_na=False, dtype=str)
customers_df = pd.read_csv("data/raw/customers_20260927.csv", keep_default_na=False, dtype=str)
transactions_df = pd.read_csv("data/raw/transactions_20260927.csv", keep_default_na=False, dtype=str)



accounts_df['currency'] = standardize_value(accounts_df['currency'], currency_mapping)
print(accounts_df['currency'].value_counts(dropna=False))
accounts_df['status'] = standardize_value(accounts_df['status'], status_mapping)
print(accounts_df['status'].value_counts(dropna=False))
customers_df['country'] = standardize_value(customers_df['country'], country_mapping)
print(customers_df['country'].value_counts(dropna=False))
transactions_df['transaction_type'] = standardize_value(transactions_df['transaction_type'], transaction_type_mapping) 
print(transactions_df['transaction_type'].value_counts(dropna=False))
