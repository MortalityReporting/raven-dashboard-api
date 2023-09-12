import json

class DocumentReference():
    resourceType: str
    status: str
    subject: any
    content: list
    def __init__(self, subject_reference, content):
        self.resourceType: str = "DocumentReference"
        self.status: str = "current"
        self.subject = subject_reference
        self.content = [content]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)

class Reference():
    reference: str
    def __init__(self, reference):
        self.reference = reference
        pass


class Content():
    attachment: any
    def __init__(self, attachment):
        self.attachment = attachment


class Attachment():
    url: str
    def __init__(self, url):
        self.url = url