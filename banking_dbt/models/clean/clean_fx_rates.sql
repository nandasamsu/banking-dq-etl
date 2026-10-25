select
rate_date::date as rate_date,
currency,
rate_to_idr::numeric(18,6) as rate_to_idr
from {{ source('staging','fx_rates')}}