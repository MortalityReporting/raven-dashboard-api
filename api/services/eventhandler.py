from api.services.fhirclient import FhirClient

'''
Event Handler
- Combines Questionnaire, QuestionnaireResponse, and Practitioner resources into an object suitable for Angular Material Tables.
'''

def getEventData():
    fhirclient = FhirClient()
    users_flat = fhirclient.searchResource("Practitioner?identifier:of-type=%7Craven-user%7C", flatten=True)# requests.get(f'{mdi_fhir_server}/Practitioner?identifier:of-type=%7Craven-user%7C', auth=auth)
    print(users_flat)
    print("---------------")
    print(len(users_flat))
    events_flat = fhirclient.searchResource("Questionnaire", flatten=True)
    registrations_flat = fhirclient.searchResource("QuestionnaireResponse", flatten=True)
    parsed = parseEventData(events_flat, registrations_flat, users_flat)
    return parsed

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

            user = list(filter(lambda user: find_user(user, subject_id), users))
            if not user:
                break
            user = user[0]
            row_obj = {
                "name": user['name'][0]['text'],
                "email": user['telecom'][0]['value'],
                "registrationId": reg['id']
            }
            for reg_item in reg['item']:
                print(reg_item)
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
    value = user_id == subject_id
    print(value)
    return user_id == subject_id