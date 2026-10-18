import pandas as pd
from banking_dq.dq_rules import check_customer, check_accounts, check_transactions

def test_c02_flags_both_duplicate_rows():
    df = pd.DataFrame({
        "source_file": ["customers_20260927.csv"] * 3,
        "source_row": [1, 2, 3],
        "customer_id": ["CIF00000154", "CIF00000154", "CIF00000155"],
        "date_of_birth": ["1980-01-01", "1980-02-01", "1990-05-15"],
        "address": ["123 Main St", "456 Elm St", "789 Oak St"],
        "country": ["ID", "ID", "ID"],
        "email": ["john@gmail.com", "johnp@yahoo.com", "jane@gmail.com"]
    })
    result = check_customer(df, "20260927")
    c02 = result[result["rule_id"] == "C02"]
    assert sorted(c02["source_row"]) == [1, 2]

def test_c02_unflags_empty_id():
    df = pd.DataFrame({
        "source_file": ["customers_20260927.csv"] * 3,
        "source_row": [1, 2, 3],
        "customer_id": ["", "", "CIF00000155"],
        "date_of_birth": ["1980-01-01", "1980-02-01", "1990-05-15"],
        "address": ["123 Main St", "456 Elm St", "789 Oak St"],
        "country": ["ID", "ID", "ID"],
        "email": ["john@gmail.com", "johnp@yahoo.com", "jane@gmail.com"]
    })
    result = check_customer(df, "20260927")
    c02 = result[result["rule_id"] == "C02"]
    assert len(c02) == 0

def test_c03_flags_invalid_date():
    df = pd.DataFrame({
        "source_file": ["customers_20260927.csv"] * 3,
        "source_row": [1, 2, 3],
        "customer_id": ["CIF00000165", "CIF00000153", "CIF00000155"],
        "date_of_birth": ["2027-01-01", "1990-02-30", "1990-05-15"],
        "address": ["123 Main St", "456 Elm St", "789 Oak St"],
        "country": ["ID", "ID", "ID"],
        "email": ["john@gmail.com", "johnp@yahoo.com", "jane@gmail.com"]
    })
    result = check_customer(df, "20260927")
    c03 = result[result["rule_id"] == "C03"]
    assert len(c03) == 2
    assert sorted(c03["source_row"]) == [1, 2]

def test_a02_flags_invalid_credit_limit():
    cust_df = pd.DataFrame({
        "source_file": ["accounts_20260927.csv"] * 3,
        "source_row": [1, 2, 3],
        "customer_id": ["CIF00000165", "CIF00000153", "CIF00000155"],
        "date_of_birth": ["2027-01-01", "1990-02-30", "1990-05-15"],
        "address": ["123 Main St", "456 Elm St", "789 Oak St"],
        "country": ["ID", "ID", "ID"],
        "email": ["john@gmail.com", "johnp@yahoo.com", "jane@gmail.com"]
    })
    df = pd.DataFrame({
            "source_file": ["accounts_20260927.csv"] * 3,
            "source_row": [1, 2, 3],
            "account_id": ["ACC000001", "ACC000002", "ACC000003"],
            "customer_id": ["CIF00000165", "CIF00000153", "CIF00000155"],
            "account_type": ["CREDIT", "CREDIT", "SAVINGS"],
            "credit_limit": ["", "", ""]
        })
    result = check_accounts(df, "20260927", cust_df)
    a02 = result[result["rule_id"] == "A02"]
    assert len(a02) == 2
    assert sorted(a02["source_row"]) == [1, 2]

def test_t01_flags_orphaned_transactions():
    df = pd.DataFrame({
            "source_file": ["transactions_20260927.csv"] * 3,
            "source_row": [1, 2, 3],
            "transaction_id": ["TXN000001", "TXN000002", "TXN000003"],
            "account_id": ["ACC000001", "ACC000002", "ACC000004"],
            "transaction_type": ["TRANSFER", "TRANSFER", "TRANSFER"],
            "amount": ["10000.00", "50000.00", "20000.00"],
            "currency": ["IDR", "IDR", "IDR"],
            "transaction_timestamp": ["2026-09-27 10:00:00", "2026-09-27 11:00:00", "2026-09-27 12:00:00"],
            "counterparty_account_id": ["ACC000005", "ACC000006", "ACC000007"],
        })
    accounts_df = pd.DataFrame({
            "source_file": ["accounts_20260927.csv"] * 3,
            "source_row": [1, 2, 3],
            "account_id": ["ACC000001", "ACC000002", "ACC000003"],
            "customer_id": ["CIF00000165", "CIF00000153", "CIF00000155"],
            "account_type": ["CREDIT", "CREDIT", "SAVINGS"],
            "credit_limit": ["", "", ""],
            "currency": ["IDR", "IDR", "IDR"],
            "status": ["ACTIVE", "ACTIVE", "ACTIVE"]
        })
    result = check_transactions(df, "20260927", accounts_df)
    t01 = result[result["rule_id"] == "T01"]
    t04 = result[result["rule_id"] == "T04"]
    assert sorted(t01["source_row"]) == [3]
    assert len(t04) == 0