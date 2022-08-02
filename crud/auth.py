from flask import Blueprint, render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/account/login')
def login():
    return render_template('login.html')


@auth.route('/account/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Wrong user or pass.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=True)
    return redirect(url_for('main.profile'))

@auth.route('/account/signup')
def signup():
    return render_template('signup.html')

@auth.route('/account/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    return 'Logout'
