from banking_dq.mappings import currency_mapping, status_mapping, country_mapping, transaction_type_mapping
from banking_dq.standardize import standardize_value
from banking_dq.extract import read_raw
from banking_dq.db import get_engine
from banking_dq.load import load_to_staging

business_date = "20260927"
accounts_df = read_raw("accounts", business_date)
customers_df = read_raw("customers", business_date)
transactions_df = read_raw("transactions", business_date)
fx_df = read_raw("fx_rates", business_date)

engine = get_engine()
load_to_staging(accounts_df, "accounts", engine)
load_to_staging(customers_df, "customers", engine)
load_to_staging(transactions_df, "transactions", engine)   
load_to_staging(fx_df, "fx_rates", engine)

accounts_df['currency'] = standardize_value(accounts_df['currency'], currency_mapping)
accounts_df['status'] = standardize_value(accounts_df['status'], status_mapping)
customers_df['country'] = standardize_value(customers_df['country'], country_mapping)
transactions_df['transaction_type'] = standardize_value(transactions_df['transaction_type'], transaction_type_mapping) 






