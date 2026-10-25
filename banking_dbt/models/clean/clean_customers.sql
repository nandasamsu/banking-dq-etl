with customers as (
    select * from {{ source('standardized', 'customers') }}
),
failed_rows as (
    select distinct source_row, business_date
    from {{ source('dq', 'exceptions') }}
    where table_name = 'customers'
)
select 
customer_id,
customer_name,
cast(date_of_birth as date) as date_of_birth,
marital_status,
gender,
city,
province, 
country,
customer_type,
risk_rating,
source_file,
source_row,
business_date
from customers c
where not exists (
    select 1 from failed_rows f
    where f.source_row = c.source_row and f.business_date = c.business_date
)