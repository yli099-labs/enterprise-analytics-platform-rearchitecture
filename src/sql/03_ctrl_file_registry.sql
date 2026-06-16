-- Public-safe reference SQL.
-- Pattern: make arrivals, contract version, schema state, and row counts queryable.

insert into ctrl.file_registry (
    registry_id,
    source_name,
    contract_id,
    source_file_name,
    file_hash,
    received_at,
    row_count,
    column_count,
    schema_status,
    load_status
)
select
    sha2(concat_ws('|', source_file_name, file_hash), 256) as registry_id,
    source_name,
    contract_id,
    source_file_name,
    file_hash,
    received_at,
    row_count,
    column_count,
    schema_status,
    'accepted' as load_status
from landing.file_manifest
where not exists (
    select 1
    from ctrl.file_registry existing
    where existing.file_hash = landing.file_manifest.file_hash
);
