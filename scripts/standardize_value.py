
import pandas as pd
import numpy as np

accounts_df = pd.read_csv("data/raw/accounts_20260927.csv", keep_default_na=False, dtype=str)
customers_df = pd.read_csv("data/raw/customers_20260927.csv", keep_default_na=False, dtype=str)
transactions_df = pd.read_csv("data/raw/transactions_20260927.csv", keep_default_na=False, dtype=str)

def standardize_value(series, mapping):
    return series.str.upper().str.strip().replace(mapping).replace('', np.nan)

currency_mapping = {
    'RM': 'MYR',
    'US$': 'USD',
    'RP': 'IDR'
    }
accounts_df['currency'] = standardize_value(accounts_df['currency'], currency_mapping)

status_mapping = {
    'AKTIF': 'ACTIVE',
    'ACTV': 'ACTIVE'
    
}
accounts_df['status'] = standardize_value(accounts_df['status'], status_mapping)

country_mapping = {
    'INDONESIA': 'ID',
    'MALAYSIA': 'MY',
    'INA': 'ID',
    'IDN': 'ID',
    'SINGAPORE': 'SG',
    'SG': 'SG',
    'MYS': 'MY'
    
}
customers_df['country'] = standardize_value(customers_df['country'], country_mapping)

transaction_type_mapping = {
    'TRF': 'TRANSFER',
    
}
transactions_df['transaction_type'] = standardize_value(transactions_df['transaction_type'], transaction_type_mapping) 
