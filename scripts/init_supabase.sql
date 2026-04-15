create table if not exists predictions (
  id bigserial primary key,
  text text not null,
  predicted_label integer not null,
  confidence double precision not null,
  explanation text,
  created_at timestamptz not null default now()
);

create table if not exists feedback (
  id bigserial primary key,
  prediction_id bigint references predictions(id) on delete cascade,
  is_correct boolean,
  comment text,
  created_at timestamptz not null default now()
);
