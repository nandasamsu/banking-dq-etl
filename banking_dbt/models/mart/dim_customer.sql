with all_ids as (
    select distinct customer_id
    from {{source('standardized','customers')}}
    where customer_id <> ''
),
clean as (
    select * from {{ ref('clean_customers')}}
)
select
a.customer_id,
c.customer_name,
c.date_of_birth,
c.marital_status,
c.gender,
c.city,
c.province,
c.country,
c.customer_type,
c.risk_rating,
c.source_file,
c.source_row,
c.business_date,
(c.customer_id is not null) as dq_passed
from all_ids a
left join clean c
on a.customer_id = c.customer_id
union all
select
'UNKNOWN' as customer_id,
null::text as customer_name,
null::date as date_of_birth,
null::text as marital_status,
null::text as gender,
null::text as city,
null::text as province,
null::text as country,
null::text as customer_type,
null::text as risk_rating,
null::text as source_file,
null::int as source_row,
null::text as business_date,
false as dq_passed
