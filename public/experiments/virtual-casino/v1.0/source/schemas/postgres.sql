-- Reference production schema. The local release uses immutable versioned files.
create table experiment (
  experiment_id text primary key,
  version text not null,
  status text not null,
  start_simulated_at timestamptz not null,
  end_simulated_at timestamptz not null,
  config_hash char(64) not null,
  code_revision text not null,
  player_manifest_hash char(64) not null,
  seed_commitment char(64) not null,
  created_at timestamptz not null default now()
);

create table world (
  world_id text primary key,
  experiment_id text not null references experiment(experiment_id),
  world_index integer not null check (world_index >= 0),
  seed_reference text not null,
  is_public_world boolean not null default false,
  status text not null,
  started_at timestamptz,
  completed_at timestamptz,
  final_state_hash char(64),
  unique (experiment_id, world_index)
);

create table player_policy (
  experiment_id text not null references experiment(experiment_id),
  player_id text not null,
  cohort_id text not null,
  policy_version text not null,
  policy_parameters_json jsonb not null,
  game_weights_json jsonb not null,
  assignment_seed_reference text not null,
  primary key (experiment_id, player_id)
);

create table ledger_event (
  world_id text not null references world(world_id),
  sequence_number bigint not null check (sequence_number > 0),
  event_type text not null,
  simulated_at timestamptz not null,
  player_id text,
  bet_id text,
  payload jsonb not null,
  previous_event_hash char(64) not null,
  event_hash char(64) not null,
  primary key (world_id, sequence_number),
  unique (world_id, bet_id),
  unique (world_id, event_hash)
);

create or replace function reject_ledger_mutation() returns trigger language plpgsql as $$
begin
  raise exception 'settled ledger events are append-only';
end $$;

create trigger ledger_no_update before update or delete on ledger_event
for each row execute function reject_ledger_mutation();

revoke insert, update, delete, truncate on ledger_event from public;
