import json, os, re

def existing_users_file(file):
    if os.path.exists(file):
        with open(file) as f:
            users = json.load(f)
    else:
        users = {}
    return users

def save_users(users, file):
    with open(file, 'w+') as save:
        json.dump(users, save)

def sanitize_title(title):
    safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', title)
    return safe_title
def sanitize_date(date):
    safe_date = re.sub(r'[^0-9]', '-', date)
    return safe_date