create table if not exists predictions (
  id bigserial primary key,
  client_prediction_id text unique,
  input_type text not null default 'text',
  text text not null,
  model_name text,
  predicted_label integer not null,
  label_name text,
  confidence double precision not null,
  risk_score double precision,
  lexical_risk_score double precision,
  probabilities jsonb,
  model_probabilities jsonb,
  suspicious_terms jsonb,
  explanation text,
  created_at timestamptz not null default now()
);

alter table predictions add column if not exists client_prediction_id text;
alter table predictions add column if not exists input_type text not null default 'text';
alter table predictions add column if not exists model_name text;
alter table predictions add column if not exists label_name text;
alter table predictions add column if not exists risk_score double precision;
alter table predictions add column if not exists lexical_risk_score double precision;
alter table predictions add column if not exists probabilities jsonb;
alter table predictions add column if not exists model_probabilities jsonb;
alter table predictions add column if not exists suspicious_terms jsonb;
alter table predictions add column if not exists explanation text;
alter table predictions add column if not exists created_at timestamptz not null default now();

create table if not exists feedback (
  id bigserial primary key,
  prediction_id bigint references predictions(id) on delete cascade,
  prediction_client_id text,
  is_correct boolean,
  comment text,
  created_at timestamptz not null default now()
);

alter table feedback add column if not exists prediction_client_id text;
alter table feedback add column if not exists is_correct boolean;
alter table feedback add column if not exists comment text;
alter table feedback add column if not exists created_at timestamptz not null default now();

create index if not exists idx_predictions_created_at on predictions(created_at desc);
create index if not exists idx_predictions_label_name on predictions(label_name);
create unique index if not exists idx_predictions_client_prediction_id
  on predictions(client_prediction_id)
  where client_prediction_id is not null;
create index if not exists idx_feedback_prediction_client_id on feedback(prediction_client_id);

alter table predictions enable row level security;
alter table feedback enable row level security;

drop policy if exists "public_predictions_insert" on predictions;
drop policy if exists "public_predictions_select" on predictions;
drop policy if exists "public_feedback_insert" on feedback;
drop policy if exists "public_feedback_select" on feedback;

create policy "public_predictions_insert"
  on predictions for insert
  to anon, authenticated
  with check (true);

create policy "public_predictions_select"
  on predictions for select
  to anon, authenticated
  using (true);

create policy "public_feedback_insert"
  on feedback for insert
  to anon, authenticated
  with check (true);

create policy "public_feedback_select"
  on feedback for select
  to anon, authenticated
  using (true);

grant usage on schema public to anon, authenticated;
grant select, insert on predictions to anon, authenticated;
grant select, insert on feedback to anon, authenticated;
grant usage, select on all sequences in schema public to anon, authenticated;
