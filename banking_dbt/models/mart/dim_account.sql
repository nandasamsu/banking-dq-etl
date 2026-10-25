with all_accounts as (
    select account_id, customer_id
    from {{ source('standardized', 'accounts')}}
    where account_id <> ''
),
clean as (
    select * from {{ ref('clean_accounts')}}
)
select
a.account_id,
a.customer_id,
c.account_type,
c.balance,
c.credit_limit,
c.currency,
c.status,
c.branch_code,
c.created_date,
c.source_file,
c.source_row,
c.business_date,
(c.account_id is not null) as dq_passed
from all_accounts a
left join clean c
on a.account_id = c.account_id
