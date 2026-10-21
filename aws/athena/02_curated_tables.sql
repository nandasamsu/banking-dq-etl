-- Curated layer: DQ exceptions written as Parquet by banking_dq/aws_job.py.
-- Parquet stores data types, so columns are typed (source_row is bigint).

CREATE DATABASE IF NOT EXISTS banking_curated;

CREATE EXTERNAL TABLE IF NOT EXISTS banking_curated.dq_exceptions (
  table_name string,
  source_file string,
  source_row bigint,
  record_id string,
  rule_id string,
  column_name string,
  failed_value string,
  dimension string,
  description string
)
PARTITIONED BY (business_date string)
STORED AS PARQUET
LOCATION 's3://nandasamsu-banking-dq/curated/dq_exception/';

MSCK REPAIR TABLE banking_curated.dq_exceptions;

-- Check: must equal SELECT COUNT(*) FROM banking_curated.dq_exceptions in PostgreSQL (1215)
SELECT business_date, COUNT(*) FROM banking_curated.dq_exceptions GROUP BY business_date;

-- Create rule catalog table to store rule metadata
CREATE EXTERNAL TABLE IF NOT EXISTS banking_curated.rule_catalog (
  rule_id string,
  dimension string,
  description string
)
STORED AS PARQUET
LOCATION 's3://nandasamsu-banking-dq/curated/rule_catalog/';
