import pandas as pd

def make_exception(df, mask, table_name, key_column, rule_id, column):
    failed = df[mask]
    return pd.DataFrame({
        "table_name": table_name,
        "source_file": failed["source_file"],
        "source_row": failed["source_row"],
        "record_id": failed[key_column],
        "rule_id": rule_id,
        "column_name": column,
        "failed_value": failed[column]
    })

def check_customer(df, business_date):
    results = []
    # C01
    mask = df["customer_id"].str.strip() == ""
    results.append(make_exception(df, mask, "customers", "customer_id","C01", "customer_id"))
    # C02
    mask = (df["customer_id"].duplicated(keep=False) & df["customer_id"].notna() & (df["customer_id"].str.strip() != ""))
    results.append(make_exception(df, mask, "customers", "customer_id","C02", "customer_id"))
    # C03
    dob = pd.to_datetime(df["date_of_birth"], errors='coerce')
    as_of_date = pd.to_datetime(business_date, format="%Y%m%d")
    mask = ((dob > as_of_date) | (dob == pd.NaT) | dob.isna())
    results.append(make_exception(df, mask, "customers", "customer_id","C03", "date_of_birth"))
    # C04
    country_codes = ["ID", "SG", "MY"]
    mask = df["country"].isin(country_codes) == False
    results.append(make_exception(df, mask, "customers", "customer_id","C04", "country"))
    # C05
    valid_email = df["email"].str.contains(r"^[\w\.-]+@[\w\.-]+\.\w+$", na=False)
    mask = ~valid_email
    results.append(make_exception(df, mask, "customers", "customer_id","C05", "email"))
    return pd.concat(results, ignore_index=True)

def check_accounts(df, business_date, customers_df):
    results = []
    # A01
    mask = ~df["customer_id"].isin(customers_df["customer_id"])
    results.append(make_exception(df, mask, "accounts", "account_id","A01", "customer_id"))
    # A02
    mask = (df['account_type'] == 'CREDIT') & (df['credit_limit'].str.strip() == '')
    results.append(make_exception(df, mask, "accounts", "account_id","A02", "credit_limit"))
    return pd.concat(results, ignore_index=True)

def check_transactions(df, business_date, accounts_df):
    results = []
    # T01
    mask = ~df["account_id"].isin(accounts_df["account_id"])
    results.append(make_exception(df, mask, "transactions", "transaction_id","T01", "account_id"))
    # T02
    amount = pd.to_numeric(df["amount"], errors="coerce")
    mask = amount.isna() | amount.le(0)
    results.append(make_exception(df, mask, "transactions", "transaction_id","T02", "amount"))
    # T03
    as_of_date = pd.to_datetime(business_date + "23:59:59", format="%Y%m%d%H:%M:%S")
    timestamp = pd.to_datetime(df["transaction_timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    mask = timestamp > as_of_date
    results.append(make_exception(df, mask, "transactions", "transaction_id","T03", "transaction_timestamp"))
    # T04
    account_currency = df.merge(accounts_df[["account_id", "currency"]].drop_duplicates("account_id"), on="account_id", how="left")["currency_y"]
    mask = (df["currency"] != account_currency) & account_currency.notna()
    results.append(make_exception(df, mask, "transactions", "transaction_id","T04", "currency"))
    # T05
    mask = (df["transaction_type"] == "TRANSFER") & (df["counterparty_account_id"].str.strip() == "")
    results.append(make_exception(df, mask, "transactions", "transaction_id","T05", "counterparty_account_id"))
    return pd.concat(results, ignore_index=True)


