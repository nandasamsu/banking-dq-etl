from banking_dq.mappings import currency_mapping, status_mapping, country_mapping, transaction_type_mapping
from banking_dq.standardize import standardize_value
from banking_dq.extract import read_raw

business_date = "20260927"
accounts_df = read_raw("accounts", business_date)
customers_df = read_raw("customers", business_date)
transactions_df = read_raw("transactions", business_date)

accounts_df['currency'] = standardize_value(accounts_df['currency'], currency_mapping)
print(accounts_df['currency'].value_counts(dropna=False))
accounts_df['status'] = standardize_value(accounts_df['status'], status_mapping)
print(accounts_df['status'].value_counts(dropna=False))
customers_df['country'] = standardize_value(customers_df['country'], country_mapping)
print(customers_df['country'].value_counts(dropna=False))
transactions_df['transaction_type'] = standardize_value(transactions_df['transaction_type'], transaction_type_mapping) 
print(transactions_df['transaction_type'].value_counts(dropna=False))

print(customers_df[["customer_id", "source_file", "source_row"]].head())