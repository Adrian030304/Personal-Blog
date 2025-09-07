import json, os

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