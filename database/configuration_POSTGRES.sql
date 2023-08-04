create table dashboard.configuration
(
    env_id text not null
        primary key,
    json   json
);