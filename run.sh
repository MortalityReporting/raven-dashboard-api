#!/bin/bash

# Export environment variables from .env file
export DB_CONN_STRING=postgresql://sacmsr4:gels-%X2MF@postgresql.icl.gtri.org:5432/cmsr4dev
export DOMAIN=dev-dk7cyfpkwowbtdbt.us.auth0.com
export API_AUDIENCE=https://raven.dev.heat.icl.gtri.org/raven-dashboard-api/
export ALGORITHMS=RS256
export ISSUER=https://dev-dk7cyfpkwowbtdbt.us.auth0.com/
export RAVEN_FHIR_SERVER=https://raven.dev.heat.icl.gtri.org/mdi-fhir-server/fhir
export RAVEN_FHIR_SERVER_BASIC_AUTH=client:secret
export MINIO_ENDPOINT=minio.dev.heat.icl.gtri.org
export MINIO_USER=ravenuser
export MINIO_SECRET=73continent85hunt
export TERM_CONN_STRING=postgresql://sainterop:riper-UAWaS@postgresql.icl.gtri.org:5432/interop_omop
export UPLOAD_FILE_PASSTHROUGH_URL=https://raven.dev.heat.icl.gtri.org/raven-import-api

# Run Uvicorn server
uvicorn api.main:app --reload