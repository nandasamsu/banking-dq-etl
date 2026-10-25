with clean as (
    select * from {{ref('clean_transactions')}}
),
account as (
    select * from {{ref('dim_account')}}
),
customer as (
    select * from {{ref('dim_customer')}}
)
select
c.transaction_id,
c.account_id,
coalesce(cu.customer_id, 'UNKNOWN') as customer_id,
c.amount,
c.currency,
c.amount * case when c.currency = 'IDR' then 1 else fx.rate_to_idr end as amount_idr,
c.transaction_type,
c.counterparty_id,
c.channel,
to_char(c.transaction_timestamp, 'YYYYMMDD')::int as date_key,
c.description,
c.status,
c.source_file,
c.source_row,
c.business_date
from clean c
left join account a
on c.account_id = a.account_id
left join customer cu
on a.customer_id = cu.customer_id
left join lateral (
	select rate_to_idr
	from {{ref('clean_fx_rates')}} cfr
	where cfr.currency  = c.currency 
	and cfr.rate_date <= c.transaction_timestamp::date
	order by cfr.rate_date desc
	limit 1
) fx on true