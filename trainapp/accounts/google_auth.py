from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

def verify_google_id_token(token, valid_client_ids):
    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
        if idinfo['aud'] not in valid_client_ids:
            return None
        return idinfo
    except ValueError:
        return None

