-- Public-safe reference SQL.
-- Pattern: convert current-state manual rules into warehouse-managed SCD2 history.

with incoming_rules as (
    select
        mapping_id,
        business_key,
        source_value,
        target_value,
        effective_from,
        effective_to,
        is_active,
        sha2(concat_ws('|',
            business_key,
            source_value,
            target_value,
            effective_from,
            coalesce(effective_to, ''),
            is_active
        ), 256) as row_hash,
        updated_at as source_modified_at
    from stg.manual_mapping_current
),
changed_rules as (
    select incoming_rules.*
    from incoming_rules
    left join ctrl.rule_history current_rules
      on incoming_rules.business_key = current_rules.business_key
     and incoming_rules.source_value = current_rules.source_value
     and current_rules.is_current = true
    where current_rules.rule_history_id is null
       or incoming_rules.row_hash <> current_rules.row_hash
)
update ctrl.rule_history current_rules
set valid_to_ts = current_timestamp,
    is_current = false
where current_rules.is_current = true
  and exists (
      select 1
      from changed_rules
      where changed_rules.business_key = current_rules.business_key
        and changed_rules.source_value = current_rules.source_value
  );

insert into ctrl.rule_history (
    rule_history_id,
    business_key,
    source_value,
    target_value,
    effective_from,
    effective_to,
    row_hash,
    valid_from_ts,
    valid_to_ts,
    is_current,
    source_modified_at,
    loaded_at
)
select
    sha2(concat_ws('|', business_key, source_value, current_timestamp), 256) as rule_history_id,
    business_key,
    source_value,
    target_value,
    effective_from,
    effective_to,
    row_hash,
    current_timestamp as valid_from_ts,
    null as valid_to_ts,
    true as is_current,
    source_modified_at,
    current_timestamp as loaded_at
from changed_rules;
