 -- table_name	total_rows	failed_rows	passed_rows	pass_rate_pct
CREATE OR REPLACE VIEW dq.scorecard_table AS
with staging_records as (
    select 'transactions' as table_name, business_date, count(*) as total_records from staging.transactions
    group by table_name, business_date
    union all
    select 'accounts'     as table_name, business_date, count(*) as total_records from staging.accounts
    group by table_name, business_date
    union all
    select 'customers'    as table_name, business_date,  count(*) as total_records from staging.customers
    group by table_name, business_date),
    failed as (
    select table_name, count(distinct(source_row)) as failed_rows, business_date 
    from dq.exceptions
    group by table_name, business_date
    )
select
s.table_name,
s.total_records,
coalesce(f.failed_rows,0) as failed_rows,
(s.total_records - coalesce(f.failed_rows,0)) as passed_rows,
round(100.0 * (s.total_records - coalesce(f.failed_rows,0))/ s.total_records, 2) as pass_rate_pct,
f.business_date 
from staging_records s
left join failed f
on s.table_name = f.table_name and s.business_date  = f.business_date;


CREATE OR REPLACE VIEW dq.scorecard_rule AS
SELECT rc.rule_id, rc.dimension, rc.description, COUNT(e.rule_id) as failed_rows
FROM dq.rule_catalog rc
left join dq.exceptions e
on rc.rule_id = e.rule_id 
and e.business_date = (select max(business_date) from dq.exceptions)
group by rc.rule_id, rc.dimension, rc.description;