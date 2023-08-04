# Environment Variables
For local development with Poetry, you can create a `.env` (which will be ignore by Git) and load it using the `poetry-dotenv-plugin`.

```
DB_CONN_STRING=postgresql://{server}:{port}/{database}
```