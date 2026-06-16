-- Public-safe reference SQL.
-- Pattern: type source data and generate deterministic keys before applying business logic.

create or replace table stg.transaction_events as
select
    sha2(concat_ws('|', event_id, line_id), 256) as event_hash_key,
    source_file_name,
    batch_id,
    event_id,
    line_id,
    cast(event_ts as timestamp) as event_ts,
    cast(business_date as date) as business_date,
    upper(trim(product_code)) as product_code,
    trim(ticket_type) as ticket_type,
    cast(quantity as number) as quantity,
    cast(net_amount as number(18, 2)) as net_amount,
    upper(trim(source_status)) as source_status,
    raw_loaded_at
from raw.transaction_events;

create or replace table stg.sensor_counts as
select
    sha2(concat_ws('|', sensor_id, count_ts, direction), 256) as sensor_count_key,
    source_file_name,
    batch_id,
    sensor_id,
    cast(count_ts as timestamp) as count_ts,
    cast(business_date as date) as business_date,
    upper(trim(location_code)) as location_code,
    upper(trim(direction)) as direction,
    cast(count_value as number) as count_value,
    raw_loaded_at
from raw.sensor_counts
where count_value >= 0;
