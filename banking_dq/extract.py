import pandas as pd

def read_raw(table_name, business_date):
    file_name = f"{table_name}_{business_date}.csv"
    file_path = f"data/raw/{file_name}"
    df = pd.read_csv(file_path, keep_default_na=False, dtype=str)
    df['source_file'] = file_name
    df['source_row'] = range(1, len(df) + 1)
    df["business_date"] = business_date
    return df