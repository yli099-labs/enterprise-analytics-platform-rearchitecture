-- Public-safe reference SQL.
-- Pattern: keep raw evidence and ingestion metadata before business interpretation.

create table raw.transaction_events (
    source_file_name varchar,
    batch_id varchar,
    event_id varchar,
    line_id varchar,
    event_ts timestamp,
    business_date date,
    product_code varchar,
    ticket_type varchar,
    quantity number,
    net_amount number(18, 2),
    source_status varchar,
    raw_loaded_at timestamp
);

create table raw.sensor_counts (
    source_file_name varchar,
    batch_id varchar,
    sensor_id varchar,
    count_ts timestamp,
    business_date date,
    location_code varchar,
    direction varchar,
    count_value number,
    raw_loaded_at timestamp
);

create table raw.manual_mapping_current (
    mapping_id varchar,
    business_key varchar,
    source_value varchar,
    target_value varchar,
    effective_from date,
    effective_to date,
    is_active varchar,
    updated_at timestamp,
    raw_loaded_at timestamp
);
