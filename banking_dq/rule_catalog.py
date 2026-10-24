import pandas as pd

RULES = pd.DataFrame([
    ("C01", "Completeness", "customer_id is empty"),
    ("C02", "Uniqueness",   "customer_id appears more than once"),
    ("C03", "Validity",     "date_of_birth is not a valid date or is in the future"),
    ("C04", "Validity",     "country is not ID, SG or MY"),
    ("C05", "Validity",     "email format is invalid"),
    ("A01", "Integrity",    "customer_id not found in customers"),
    ("A02", "Completeness", "CREDIT account has no credit_limit"),
    ("A03", "Validity",     "created_date is not a valid timestamp"),
    ("T01", "Integrity",    "account_id not found in accounts"),
    ("T02", "Accuracy",     "amount is empty, zero or negative"),
    ("T03", "Timeliness",   "transaction_timestamp is after the business date"),
    ("T04", "Consistency",  "posting currency differs from account currency"),
    ("T05", "Completeness", "TRANSFER has no counterparty_account_id"),
    ("T06", "Validity",     "transaction_timestamp is not a valid timestamp"),
    ("T07", "Uniqueness",   "transaction_id appears more than once")
], columns=["rule_id", "dimension", "description"])