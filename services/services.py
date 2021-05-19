import csv
from flask import jsonify


path = "database/users.csv"
fieldnames = ["id", "name", "email", "password", "age"]

def write_csv(data):
    with open(path, "w") as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows(data)


def show_users():

    with open(path) as f:
        return list(csv.DictReader(f))


def handle_signup(user_data):
    users = show_users()
    id = 1

    for user in users:
        if user_data["email"] == user["email"]:
            return {}, 422

    if len(users) > 0:
        id = int(users[-1]["id"]) + 1

    with open(path, "a+") as f:        
        f.seek(0)
        
        writer = csv.DictWriter(f, fieldnames)

        user = {'id': id, **user_data}
        writer.writerow(user)

    del user["password"]

    return jsonify(user), 201


def handle_login(user_data):
    users = show_users()

    for user in users:
        if user_data["email"] == user["email"] and user_data["password"] == user["password"]:
            del user["password"]
            return jsonify(user)

    return {"error": "Invalid credentials"}, 401


def handle_update_user(user_id, attributes):
    users = show_users()
    updated_user = {}

    for user in users:
        if int(user["id"]) == user_id:

            for attribute in attributes.keys():
                if attribute in fieldnames:
                    user[attribute] = attributes[attribute]

            write_csv(users)

            updated_user = user
            del updated_user["password"]
            return updated_user, 200

    return {"error": "User not exists"}, 404


def handle_delete_user(user_id):
    users = show_users()

    for i, user in enumerate(users):
        if user_id == int(user["id"]):
            users.pop(i)
            write_csv(users)
            return {}, 204
    
    return {"error": "User not exists"}, 404
