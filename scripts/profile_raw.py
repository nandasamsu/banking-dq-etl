import pandas as pd
import numpy as np

# Profile raw data files and print the number of distinct values and empty values for each column.
file_list = [
    "data/raw/transactions_20260927.csv",
    "data/raw/accounts_20260927.csv",
    "data/raw/customers_20260927.csv",
    "data/raw/fx_rates_20260927.csv"
]

for file in file_list:
    df = pd.read_csv(file, keep_default_na=False, dtype=str)
    print(f"File: {file}")
    print(f"Shape: {df.shape}")
    for column in df.columns:
        distinct = df[column].nunique()
        empty_values = (df[column].str.strip() == "").sum()
        print(f"{column:<25} distinct: {distinct} | empty values: {empty_values}")
    print("\n")






