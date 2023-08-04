from fastapi.testclient import TestClient
import json
from api.main import app

client = TestClient(app)

test_json = '{ "version": "", "title": "Raven", "ravenFhirServer": "https://raven.dev.heat.icl.gtri.org/mdi-fhir-server/fhir", "ravenFhirServerBasicAuth": "client:secret", "ravenImportApi": "https://raven.dev.heat.icl.gtri.org/raven-import-api/upload-xlsx-file", "fhirValidator": "https://dev.heat.icl.gtri.org/fhir-validator-service/fhir", "blueJayServerBase": "https://bluejay.heat.icl.gtri.org/mdi-fhir-server", "adminRedirectUrl": "https://localhost:4200/admin-panel", "adminLogoutUrl": "https://localhost:4200/", "logFhirRequests": false }'

def test_get_settings():
    response = client.get('/config')
    response_json = response.json()

    print(response_json)

    assert response_json == test_json
