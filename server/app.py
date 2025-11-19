#!/usr/bin/env python3

from flask import Flask, request, session, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Needed for session cookies
app.secret_key = "super-secret-key"

CORS(app, supports_credentials=True)
migrate = Migrate(app, db)

db.init_app(app)


# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")

    user = User.query.filter_by(username=username).first()
    if not user:
        return make_response({"error": "Invalid username"}, 401)

    session["user_id"] = user.id

    return make_response(user.to_dict(), 200)


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)
    return make_response("", 204)


# -----------------------------
# CHECK SESSION
# -----------------------------
@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')

    if not user_id:
        return {}, 401

    user = User.query.get(user_id)

    if not user:
        return {}, 401

    return user.to_dict(), 200


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(port=5555)
