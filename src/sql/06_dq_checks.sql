-- Public-safe reference SQL.
-- Pattern: store quality signals as reviewable data, not hidden job logs.

-- Duplicate transaction natural keys after deterministic key creation.
select
    'DQ_TXN_001' as dq_rule_id,
    event_hash_key as business_key,
    count(*) as detected_value,
    'one accepted current row per event line' as expected_condition
from stg.transaction_events
group by event_hash_key
having count(*) > 1;

-- Active mapping effective windows should not overlap for the same governed key.
select
    'DQ_CTRL_001' as dq_rule_id,
    concat(a.business_key, '|', a.source_value) as business_key,
    concat(a.mapping_id, ' overlaps ', b.mapping_id) as detected_value,
    'non-overlapping active effective windows' as expected_condition
from stg.manual_mapping_current a
join stg.manual_mapping_current b
  on a.business_key = b.business_key
 and a.source_value = b.source_value
 and a.mapping_id < b.mapping_id
 and a.is_active = 'Y'
 and b.is_active = 'Y'
 and a.effective_from <= coalesce(b.effective_to, date '9999-12-31')
 and b.effective_from <= coalesce(a.effective_to, date '9999-12-31');

-- Curated fact grain should stay unique.
select
    'DQ_CUR_001' as dq_rule_id,
    concat(business_date, '|', analytics_entity_code) as business_key,
    count(*) as detected_value,
    'one row per business_date and analytics_entity_code' as expected_condition
from cur.daily_visitorship
group by business_date, analytics_entity_code
having count(*) > 1;

-- Schema changes should be visible before curated publication.
select
    'DQ_SCHEMA_001' as dq_rule_id,
    source_file_name as business_key,
    schema_status as detected_value,
    'schema_status = contract_match' as expected_condition
from ctrl.file_registry
where schema_status <> 'contract_match';
