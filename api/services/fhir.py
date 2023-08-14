import requests
from requests.auth import HTTPBasicAuth
import os
from api.utils.setup import set_up
import json

def getEventData():
    config = set_up()
    parsed_auth = config["RAVEN_FHIR_SERVER_BASIC_AUTH"].split(":")
    mdi_fhir_server = config["RAVEN_FHIR_SERVER"]
    auth = HTTPBasicAuth(parsed_auth[0], parsed_auth[1])
    practitioners = requests.get(f'{mdi_fhir_server}/Practitioner?identifier:of-type=%7Craven-user%7C', auth=auth)
    questionnaires = requests.get(f'{mdi_fhir_server}/Questionnaire', auth=auth)
    questionnaireResponses = requests.get(f'{mdi_fhir_server}/QuestionnaireResponse', auth=auth)
    # merged_bundle = mergeBundles([practitioners.json(), questionnaires.json(), questionnaireResponses.json()])
    events_flat = flattenBundle(questionnaires.json())
    registrations_flat = flattenBundle(questionnaireResponses.json())
    users_flat = flattenBundle(practitioners.json())

    parsed = parseEventData(events_flat, registrations_flat, users_flat)
    return parsed

def mergeBundles(bundles: list):
    merged_bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": []
    }
    for bundle in bundles:
        merged_bundle["entry"] += bundle["entry"]
    return merged_bundle

def flattenBundle(bundle):
    resource_list = []
    for entry in bundle['entry']:
        resource_list.append(entry["resource"])
    return resource_list

def parseEventData(events: list, registrations: list, users: list):
    event_data = {"events": []}
    for event in events:
        # Setup Event Data
        event_obj = {
            "title": event['title'],
            "id": event['id'],
            "cols": {},  # Column Headers
            "rows": []
        }
        for item in event['item']:
            event_obj['cols'][item['linkId']] = item['text']
        
        this_events_registrations = filter(lambda reg: filter_by_event(reg, event_obj['id']), registrations)

        for reg in this_events_registrations:
            subject_id = reg['subject']['reference'].split("/")[-1]
            user = list(filter(lambda user: find_user(user, subject_id), users))[0]
            row_obj = {
                "name": user['name'][0]['text'],
                "email": user['telecom'][0]['value'],
            }
            for reg_item in reg['item']:
                row_obj[reg_item["linkId"]] = reg_item["answer"][0]["valueCoding"]["code"]
            
            event_obj['rows'].append(row_obj)
        event_data["events"].append(event_obj)
    return event_data


# Filter Registrations by Event, for use in filter()
def filter_by_event(registration, event_id):
    questionnaire_reference_id = registration['questionnaire'].split("/")[-1]
    print(questionnaire_reference_id)
    print(event_id)
    return questionnaire_reference_id == event_id

# Filter Users by Registration Subject, for use in filter()
def find_user(user, subject_id):
    user_id = user['id']
    return user_id == subject_id