Possible Transitions
Not Started -> In Progress
In Progress -> Pending Review
In Progress -> Complete
Pending Review -> Complete
Pending Review -> Document Rejected
Document Rejected -> Incomplete (functionally the same as starting over)


Not Started -> Incomplete // On launch of a test, handled by the test container entirely.
Incomplete -> Pending Review // On submission of a document, handled by the test container entirely.
Incomplete -> Complete // On completion of a test, emitted by the component (e.g., search edrs on a given criteria), caught by container
Pending Review -> Complete // Admin panel manual change after review.
Pending Review -> Document Rejected // Admin panel manual change after review.
Document Rejected -> Incomplete (functionally the same as starting over) // On launch of a test that is in the recected state, otherwise same as first one



---
User profile is created on MDI FHIR Server (Practitioner)
On generation, create new copy "golden" document on BlueJay (Set of resources)
Retrieve the new BlueJay update document ID(s)
Store the Bluejay document ID in the user profile resource
