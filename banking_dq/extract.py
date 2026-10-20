import pandas as pd

def read_raw(table_name, business_date, base_path="data/raw"):
    file_name = f"{table_name}_{business_date}.csv"
    if base_path.startswith('s3://'):
        file_path = f"{base_path}/{table_name}/business_date={business_date}/{file_name}"
    else: 
        file_path = f"{base_path}/{file_name}"
    df = pd.read_csv(file_path, keep_default_na=False, dtype=str)
    df['source_file'] = file_name
    df['source_row'] = range(1, len(df) + 1)
    df["business_date"] = business_date
    return df