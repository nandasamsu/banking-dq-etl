import pandas as pd

def read_raw(table_name, business_date):
    """
    Read raw data from CSV files based on the table name and business date.
    
    Args:
        file_name (str): The name of the table (e.g., "accounts", "customers", "transactions").
        business_date (str): The business date in the format YYYYMMDD.
        file_path (str): The path to the raw data file.
        df (pd.DataFrame): The DataFrame containing the raw data.
        df['source_file'] (str): The name of the source file.
        df['source_row'] (int): The row number in the source file. add range(1, len(df) + 1) to create a new column 'source_row'that contains the row number for each record in the DataFrame starting from 1 until the length of the DataFrame + 1.
    Returns:
        pd.DataFrame: A DataFrame containing the raw data.
    """
    file_name = f"{table_name}_{business_date}.csv"
    file_path = f"data/raw/{file_name}"
    df = pd.read_csv(file_path, keep_default_na=False, dtype=str)
    df['source_file'] = file_name
    df['source_row'] = range(1, len(df) + 1)
    return df