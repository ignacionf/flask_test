from flask import Blueprint, url_for, request, flash, jsonify, Response, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask import jsonify

from .models import User
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/v1/account/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return Response({"error": "User/Pass invalid"}, status=403)

    login_user(user, remember=True)
    return jsonify({"user": user.name})


@auth.route("/v1/account/signup", methods=["POST"])
def signup_post():
    print("lala")
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
        return Response({"error": "User already exist"}, status=400)

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="sha256"),
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"user": new_user.name})


@auth.route("/v1/account/logout")
def logout():
    logout_user()
    # ugly... but...
    return redirect(url_for("main.index"))


@auth.route("/v1/account/")
def account():
    users = []

    for user in User.query.all():
        users.append(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "url": url_for("auth.account_change", user_id=user.id),
                "view": url_for("main.account_view", user_id=user.id),
            }
        )
    return jsonify(users)


@auth.route("/v1/account/<user_id>", methods=["DELETE"])
def account_delete(user_id):
    User.query.filter_by(id=int(user_id)).delete()
    db.session.commit()
    return jsonify({})


@auth.route("/v1/account/<user_id>", methods=["PUT"])
def account_change(user_id):

    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    user = User.query.filter_by(id=int(user_id)).first()
    user.email = email
    user.name = name

    if password:
        user.password = generate_password_hash(password, method="sha256")

    db.session.commit()
    return jsonify({})
