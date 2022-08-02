from flask import Blueprint, render_template
from flask_login import login_required, current_user

from . import db
from .models import User

main = Blueprint("main", __name__)


@main.route("/")
def index():

    if current_user.is_authenticated:
        user = current_user
    else:
        user = None
    return render_template("index.html", user=user)


@main.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user)


@main.route("/account/<user_id>")
@login_required
def account_view(user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    return render_template("account_change.html", user=current_user, edit_user=user)


@main.route("/account/login")
def login():
    return render_template("login.html")


@main.route("/account/signup")
def signup():
    return render_template("signup.html")
