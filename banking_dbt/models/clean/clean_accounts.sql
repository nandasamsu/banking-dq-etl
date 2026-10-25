with accounts as (
    select * from {{ source('standardized', 'accounts') }}
),
failed_rows as (
    select distinct source_row, business_date
    from {{ source('dq', 'exceptions') }}
    where table_name = 'accounts'
)
select 
account_id,
customer_id,
account_type,
cast(balance as numeric(18,2)),
nullif(credit_limit,'') as credit_limit,
currency,
status,
branch_code,
cast(created_date as date),
source_file,
source_row,
business_date
from accounts a
where not exists (
    select 1 from failed_rows f
    where f.source_row = a.source_row and f.business_date = a.business_date
)