import requests
from requests.auth import HTTPBasicAuth
from api.utils.setup import set_up

class FhirClient():
    server_base: str
    basic_auth: HTTPBasicAuth
    content_type_header: any

    def __init__(self):
        config = set_up()
        basic_auth_str = config["RAVEN_FHIR_SERVER_BASIC_AUTH"].split(":")
        self.basic_auth = HTTPBasicAuth(basic_auth_str[0], basic_auth_str[1])
        self.server_base = config["RAVEN_FHIR_SERVER"]
        self.content_type_header = {'Content-type': 'application/fhir+json'}

    def createResource(self, resource_type, resource):
        response = requests.post(f'{self.server_base}/{resource_type}', resource, auth=self.basic_auth, headers=self.content_type_header).json()
        return response

    def updateResource(self, resource_type, id, resource):
        return {}

    def readResource(self, resource_type, id):
        return {}

    def searchResource(self, resource_type, parameters = None, flatten = False):
        searchset = requests.get(f'{self.server_base}/{resource_type}_count=100', auth=self.basic_auth).json()
        if flatten:
            resource_list = []
            for entry in searchset['entry']:
                resource_list.append(entry["resource"])
            return resource_list
        return searchset
