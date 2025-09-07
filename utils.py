from base64 import b64decode, b64encode
from flask import Response

def check_auth(auth_header, USERNAME, PASSWORD):
    if not auth_header or not auth_header.startswith("Basic "):
        return False
    encoded = auth_header.split(" ", 1)[1]
    try:
        decoded = b64decode(encoded).decode("utf-8")
    except Exception:
        return False
    username, password = decoded.split(":", 1)
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        "Authentication required",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )