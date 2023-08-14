import os

def set_up():
    """Sets up configuration for the app"""
    config = {
        "DB_CONN_STRING": os.getenv("DB_CONN_STRING"),
        "RAVEN_FHIR_SERVER": os.getenv("RAVEN_FHIR_SERVER"),
        "RAVEN_FHIR_SERVER_BASIC_AUTH": os.getenv("RAVEN_FHIR_SERVER_BASIC_AUTH")
    }
    return config
 
def set_up_token():
    """Sets up configuration for the app"""
    config = {
        "DOMAIN": os.getenv("DOMAIN", "your.domain.com"),
        "API_AUDIENCE": os.getenv("API_AUDIENCE", "your.audience.com"),
        "ISSUER": os.getenv("ISSUER", "https://your.domain.com/"),
        "ALGORITHMS": os.getenv("ALGORITHMS", "RS256"),
    }
    return config