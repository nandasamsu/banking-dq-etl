with days as (
    select generate_series(
        '2020-01-01'::date,
        '2030-12-31'::date,
        interval '1 day'
    )::date as d
)

select to_char(d,'YYYYMMDD')::int as date_key,
d as date,
extract(day from d)::int as "day", 
extract(isodow from d)::int as day_of_week,
extract(isodow from d) in (6,7) as is_weekend,
extract(month from d)::int as "month",
to_char(d, 'FMMonth') as month_name,
extract(quarter from d)::int as "quarter",
extract(year from d)::int as "year"
from days
