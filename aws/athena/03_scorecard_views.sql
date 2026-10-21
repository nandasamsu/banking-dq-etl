-- table_name	total_rows	failed_rows	passed_rows	pass_rate_pct
CREATE OR REPLACE VIEW banking_curated.scorecard_table AS with staging_records as (
		select 'transactions' as table_name,
			business_date,
			count(*) as total_records
		from banking_raw.transactions
		group by 1,2
		union all
		select 'accounts' as table_name,
			business_date,
			count(*) as total_records
		from banking_raw.accounts
		group by 1,2
		union all
		select 'customers' as table_name,
			business_date,
			count(*) as total_records
		from banking_raw.customers
		group by 1,2
	),
	failed as (
		select table_name,
			business_date,
            count(distinct(source_row)) as failed_rows
		from banking_curated.dq_exceptions
		group by 1,2
	)
select s.table_name,
	s.total_records,
	coalesce(f.failed_rows, 0) as failed_rows,
	(s.total_records - coalesce(f.failed_rows, 0)) as passed_rows,
	round(
		100.0 * (s.total_records - coalesce(f.failed_rows, 0)) / s.total_records,
		2
	) as pass_rate_pct,
	s.business_date
from staging_records s
	left join failed f on s.table_name = f.table_name
	and s.business_date = f.business_date;


CREATE OR REPLACE VIEW banking_curated.scorecard_rule AS
SELECT rc.rule_id,
	rc.dimension,
	rc.description,
	COUNT(e.rule_id) as failed_rows
FROM banking_curated.rule_catalog rc
	left join banking_curated.dq_exceptions e on rc.rule_id = e.rule_id
	and e.business_date = (
		select max(business_date)
		from banking_curated.dq_exceptions
	)
group by 1,2,3;