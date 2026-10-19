# Banking DQ ETL

![tests](https://github.com/nandasamsu/banking-dq-etl/actions/workflows/tests.yml/badge.svg)

A data quality pipeline for banking data, built with Python and PostgreSQL. It loads raw customer, account and transaction files, checks them against 12 data quality rules, and produces a scorecard showing the pass rate per table and the number of failures per rule.

I work on SQL-based ETL and data quality in banking. I built this project to rebuild that kind of process in Python with modern data engineering practices: version control, lineage, rerunnable loads and reproducible setup.

All data is synthetic. Nothing comes from a real bank.

## Results

DQ scorecard for business date '2026-09-27':

| Table         | Total rows | Failed rows | Passed rows | Pass rate |
| ---           | ---:       | ---:        | ---:        | ---:      |
| accounts      | 1,500      | 37          | 1,463       | 97.53%    |
| transactions  | 20,160     | 1,100       | 19,060      | 94.54%    |
| customers     | 1,020      | 62          | 958         | 93.92%    |

Failures per rule:

| Rule | Dimension | Description | Failed rows |
| --- | --- | --- | ---: |
| T04 | Consistency | posting currency differs from account currency | 328 |
| T02 | Accuracy | amount is empty, zero or negative | 299 |
| T01 | Integrity | account_id not found in accounts | 241 |
| T05 | Completeness | TRANSFER has no counterparty_account_id | 148 |
| T03 | Timeliness | transaction_timestamp is after the business date | 100 |
| C05 | Validity | email format is invalid | 27 |
| A01 | Integrity | customer_id not found in customers | 22 |
| C02 | Uniqueness | customer_id appears more than once | 20 |
| C03 | Validity | date_of_birth is not a valid date or is in the future | 15 |
| A02 | Completeness | CREDIT account has no credit_limit | 15 |
| C01 | Completeness | customer_id is empty | 0 |
| C04 | Validity | country is not ID, SG or MY | 0 |

C04 has 0 failures because standardization maps every country variant in the raw file (`INDONESIA`, `INA`, `SGP`, ...) to an ISO code before validation runs.

## How it works

```
raw CSV files
   │  extract.py      read as text, add source_file, source_row, business_date
   ▼
staging.*            exact copy of the raw files (evidence)
   │  standardize.py  trim, upper-case, map codes (RP → IDR, AKTIF → ACTIVE, ...)
   ▼
dq_rules.py          12 rules across 7 DQ dimensions
   │
   ▼
dq.exceptions        one row per failed record per rule, with lineage
   │
   ▼
dq.scorecard_table   pass rate per table
dq.scorecard_rule    failures per rule (every rule listed, including 0)
```

The whole run is one command: `python -m banking_dq.pipeline`.

## Design decisions

- **Staging is loaded before standardizing.** Staging stays an exact copy of the source files, so it can serve as evidence of what the source system actually sent.
- **Every exception keeps its lineage.** `source_file` and `source_row` point back to the exact line in the raw CSV, so a failed record can be traced and reported to the data owner.
- **Reruns are idempotent.** Before loading exceptions, the pipeline deletes any rows for the same `business_date`. Running the same day twice gives the same result, with no duplicates.
- **Scorecard views are rebuilt every run.** Staging tables are dropped with `CASCADE` and the views are recreated from `sql/scorecard.sql` at the end of the pipeline.
- **DQ checks run after standardization.** This avoids false alarms from formatting differences (for example `' id '` vs `ID`).
- **Rules don't cascade into each other.** For example T04 only compares currencies when the account exists, so an orphan transaction is counted once under T01 and not again under T04.
- **Rule logic is tested.** pytest tests feed each rule a small hand-made DataFrame where the correct answer is known in advance, including edge cases: empty IDs are not counted as duplicates, only CREDIT accounts need a credit limit, and an orphan transaction is flagged by T01 but not double-counted by T04.
- **Assumption for T04:** `transactions.currency` is the posting currency, which must match the account currency.

## Project layout

```
banking_dq/
  extract.py        read raw CSVs and add lineage columns
  standardize.py    generic value standardization
  mappings.py       code mappings (currency, status, country, transaction type)
  dq_rules.py       the 12 DQ rules
  rule_catalog.py   rule ID, dimension and description
  load.py           load to PostgreSQL, run SQL files
  db.py             database connection from .env
  pipeline.py       runs everything end to end
sql/scorecard.sql   scorecard views
scripts/profile_raw.py   read-only profiling of the raw files
data/raw/           synthetic source files for 2026-09-27
tests/              pytest tests for the DQ rules
```

## How to run

Requirements: Python 3.12, Docker.

```bash
# 1. Start PostgreSQL
docker run --name banking-postgres \
  -e POSTGRES_USER=etl_user -e POSTGRES_PASSWORD=changeme -e POSTGRES_DB=banking_dw \
  -p 5432:5432 -d postgres:16

# 2. Set up Python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env              # edit DB_PASSWORD if you changed it

# 3. Run the pipeline
python -m banking_dq.pipeline

# 4. Run the tests
python -m pytest -v
```

Then query the results:

```sql
SELECT * FROM dq.scorecard_table;
SELECT * FROM dq.scorecard_rule ORDER BY failed_rows DESC;
```

## Limitations and next steps

- **No history yet.** The scorecard shows the latest business date only. Next: a `dq.scorecard_history` table to track pass rates over time.
- **No clean layer or reporting mart yet.** Next: write passed records to a clean schema and build a reporting mart on top.
- **Cloud version.** Next: run the same pipeline on AWS (S3, Glue, Athena).
