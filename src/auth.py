from flask import Blueprint, request
from flask import json
from flask.json import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from src.models import User, Bookmark, db

from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    if len(password) < 6 :
        return jsonify({"error": "password is too short"}), HTTP_400_BAD_REQUEST

    else:
        pwd_hash = generate_password_hash(password)

    if len(username) < 3:
        return jsonify({"error": 
                        "the username is too short, it must be at least 6 characters"}), HTTP_400_BAD_REQUEST
    
    elif not username.isalnum() or " " in username:
        return jsonify({"error":
                        "the username must not contain spaces and must be alphanumeric"}), HTTP_400_BAD_REQUEST

    elif User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "username already taken"}), HTTP_409_CONFLICT


    if not validators.email(email):
        return jsonify({"error": "the email provided is not valid"}), HTTP_400_BAD_REQUEST

    elif User.query.filter_by(email=email).first() is not None:
        return jsonify ({"error": "email is already taken"}), HTTP_409_CONFLICT
 
    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "user created",
        "user": {
            "username": username,
            "email": email
            }
        }), HTTP_201_CREATED


@auth.get("/me")
def me():
    return "User me"
