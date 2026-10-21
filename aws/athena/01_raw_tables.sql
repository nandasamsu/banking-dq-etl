-- Raw layer: exact copy of the source CSV files in S3.
-- All columns are string on purpose: the DQ rules decide what is valid.
-- Run each statement separately in the Athena query editor (region ap-southeast-1).

CREATE DATABASE IF NOT EXISTS banking_raw;

CREATE EXTERNAL TABLE IF NOT EXISTS banking_raw.customers (
  customer_id string, customer_name string, date_of_birth string,
  marital_status string, gender string, address string, city string,
  province string, country string, zipcode string, id_number string,
  id_type string, customer_type string, email string, phone_number string,
  risk_rating string, created_date string, updated_date string
)
PARTITIONED BY (business_date string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION 's3://nandasamsu-banking-dq/raw/customers/'
TBLPROPERTIES ('skip.header.line.count'='1');

CREATE EXTERNAL TABLE IF NOT EXISTS banking_raw.accounts (
  account_id string, customer_id string, account_type string, balance string,
  credit_limit string, currency string, status string, branch_code string,
  created_date string
)
PARTITIONED BY (business_date string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION 's3://nandasamsu-banking-dq/raw/accounts/'
TBLPROPERTIES ('skip.header.line.count'='1');

CREATE EXTERNAL TABLE IF NOT EXISTS banking_raw.transactions (
  transaction_id string, account_id string, amount string, currency string,
  transaction_type string, counterparty_account_id string, channel string,
  transaction_timestamp string, description string, status string
)
PARTITIONED BY (business_date string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION 's3://nandasamsu-banking-dq/raw/transactions/'
TBLPROPERTIES ('skip.header.line.count'='1');

CREATE EXTERNAL TABLE IF NOT EXISTS banking_raw.fx_rates (
  rate_date string, currency string, rate_to_idr string
)
PARTITIONED BY (business_date string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION 's3://nandasamsu-banking-dq/raw/fx_rates/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- Register the business_date=... folders as partitions (rerun after adding a new date)
MSCK REPAIR TABLE banking_raw.customers;
MSCK REPAIR TABLE banking_raw.accounts;
MSCK REPAIR TABLE banking_raw.transactions;
MSCK REPAIR TABLE banking_raw.fx_rates;

-- Checks: expect customers 1020, accounts 1500, transactions 20160, fx_rates 318
SELECT business_date, COUNT(*) FROM banking_raw.customers GROUP BY business_date;
SELECT business_date, COUNT(*) FROM banking_raw.accounts GROUP BY business_date;
SELECT business_date, COUNT(*) FROM banking_raw.transactions GROUP BY business_date;
SELECT business_date, COUNT(*) FROM banking_raw.fx_rates GROUP BY business_date;
