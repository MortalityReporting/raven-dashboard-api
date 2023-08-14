# Admin Panel Endpoint

```
{service_url}/admin-panel
```
**Requires Scope:** `admin`

This endpoint provides authorized users with a full report of testing events, served in a format easily converted to an Angular Material Table. Keys for column headers and row by row test statuses are the `linkId` of a given test item in the source FHIR resources.

**REQUEST**
```
GET /admin-panel
```
**RESPONSE**
```
{
    "events": [
        {
            "id": "1234",
            "title": "Example Testing Event - Feb 01, 2024",
            "cols": {
                "1": "Onboarding",
                "2": "Search EDRS",
                "3": "Update EDRS"
            },
            "rows": [
                {
                    "name": "John Doe",
                    "email": "example@gmail.com",
                    "1": "complete",
                    "2": "in-progress",
                    "3": "in-progress"
                },
                {
                    "name": "Bob Smith",
                    "email": "bob@gmail.com",
                    "1": "complete",
                    "2": "complete",
                    "3": "in-progress"
                }
            ]
        }
    ]
}
```