from flask import Flask, request, jsonify
from .services.services import show_users, handle_signup, handle_login, handle_update_user, handle_delete_user

app = Flask(__name__)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    return handle_signup(data)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    return handle_login(data)


@app.route("/profile/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    data = request.get_json()

    return handle_update_user(user_id, data)


@app.route("/profile/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    return handle_delete_user(user_id)


@app.route("/users")
def all_users():
    return jsonify(show_users())