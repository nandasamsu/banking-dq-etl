with transactions as (
    select * from {{ source('standardized', 'transactions') }}
),
failed_rows as (
    select distinct source_row, business_date
    from {{ source('dq', 'exceptions') }}
    where table_name = 'transactions'
)
select 
transaction_id,
account_id,
cast(amount as numeric(18,2)),
currency,
transaction_type,
nullif(counterparty_account_id,'') as counterparty_id,
channel,
cast(transaction_timestamp as timestamp),
description,
status,
source_file,
source_row,
business_date
from transactions t
where not exists (
    select 1 from failed_rows f
    where f.source_row = t.source_row and f.business_date = t.business_date
)