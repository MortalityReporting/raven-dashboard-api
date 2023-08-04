# Raven Dashboard API

This is a small supporting API for the Raven Dashboard to allow the configuration of secured endpoints and serve run time configuration if desired.

## Setting up a Development Environment
This project was initialized using Poetry. If you are using Poetry, you will also need the poetry-dotenv-plugin (or another way to manage your Poetry shell environment variables). For more information on environment configuration, please see `env.md`.

To run in Poetry, you must enter the shell to execute uvicorn without any barriers:
```
poetry install
poetry shell
uvicorn api.main:app --reload
```

## Database/Schema
As this is a lightweight API intended to run alongside other components, it assumes the use of a shared database server across multiple Raven components. As such, the schema in the scripts and code defaults to `dashboard` to separate its tables from other information.

## Endpoints

### /config?env={env_name}
The `/config` endpoint retrieves an arbitray JSON file (which should be aligned with the configuration JSON in the Raven Dashboard). You can setup multiple environments and request them via the `env={env_name}` parameter. `dev` is the default in the API code.

Examples:
* `https://{server_base}/config` will perform a SQL select on the database where the `env_id` column equals `dev`.
* `https://{server_base}/config?env=prod` will perform a SQL select on the database where the `env_id` column equals `prod`.

In the Raven Dashboard code you may set the connection string to include the environment you wish to use. This allows testing with multiple environment configurations. For more information, please see the Raven Dashboard itself.

### /admin *IN DEVELOPMENT*
In development.
