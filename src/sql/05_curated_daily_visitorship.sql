-- Public-safe reference SQL.
-- Pattern: publish a stable curated grain using effective-dated rules and opening-hour controls.

create or replace table cur.daily_visitorship as
with mapped_counts as (
    select
        s.business_date,
        m.target_value as analytics_entity_code,
        s.count_ts,
        s.count_value,
        s.batch_id,
        h.open_time,
        h.close_time
    from stg.sensor_counts s
    join ctrl.rule_history m
      on m.business_key = 'location_to_zone'
     and m.source_value = s.location_code
     and m.is_current = true
     and s.business_date between m.effective_from and coalesce(m.effective_to, date '9999-12-31')
    left join ctrl.opening_hours h
      on h.calendar_date = s.business_date
     and h.location_code = s.location_code
    where s.direction = 'IN'
),
transaction_counts as (
    select
        business_date,
        count(distinct event_hash_key) as transaction_count
    from stg.transaction_events
    group by business_date
)
select
    business_date,
    analytics_entity_code,
    sum(count_value) as total_visitors,
    sum(case
        when cast(count_ts as time) between open_time and close_time then count_value
        else 0
    end) as open_hours_visitors,
    coalesce(max(transaction_count), 0) as transaction_count,
    listagg(distinct batch_id, '|') as source_batches,
    current_timestamp as curated_at
from mapped_counts
left join transaction_counts using (business_date)
group by business_date, analytics_entity_code;
