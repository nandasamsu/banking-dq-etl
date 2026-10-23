import pandas as pd
from banking_dq.mappings import currency_mapping, status_mapping, country_mapping, transaction_type_mapping
from banking_dq.standardize import standardize_value
from banking_dq.dq_rules import check_accounts, check_customer, check_transactions
from banking_dq.rule_catalog import RULES

def standardize_all(customers_df, accounts_df, transactions_df):
    customers_df = customers_df.copy()
    accounts_df = accounts_df.copy()
    transactions_df = transactions_df.copy()
    accounts_df['currency'] = standardize_value(accounts_df['currency'], currency_mapping)
    accounts_df['status'] = standardize_value(accounts_df['status'], status_mapping)
    customers_df['country'] = standardize_value(customers_df['country'], country_mapping)
    transactions_df['transaction_type'] = standardize_value(transactions_df['transaction_type'], transaction_type_mapping) 
    transactions_df["currency"] = standardize_value(transactions_df["currency"], currency_mapping)
    accounts_df["account_type"] = standardize_value(accounts_df["account_type"], {})
    return customers_df, accounts_df, transactions_df


def run_dq(customers_df, accounts_df, transactions_df, business_date):
    customers_df, accounts_df, transactions_df = standardize_all(customers_df, accounts_df, transactions_df)

    customer_exceptions_df = check_customer(customers_df, business_date)
    account_exceptions_df = check_accounts(accounts_df, business_date, customers_df)
    transaction_exceptions_df = check_transactions(transactions_df, business_date, accounts_df)

    all_exceptions_df = pd.concat([customer_exceptions_df, account_exceptions_df, transaction_exceptions_df], ignore_index=True,)
    all_exceptions_df["business_date"] = business_date
    all_exceptions_df = all_exceptions_df.merge(RULES, on="rule_id", how="left")

    return all_exceptions_df