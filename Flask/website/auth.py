from flask import Blueprint, render_template, request, flash, redirect, url_for

from . import db
from .modles import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


# @auth.route('/home', methods=['GET', 'POST'])
# @login_required
# def home():
#     return render_template("home.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password or Email', category='error')
        else:
            flash('User Does not Present', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('Email')
        firstname = request.form.get('firstName')
        lastname = request.form.get('lastName')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('User Already Exists', category='error')
        elif len(email) <= 3:
            flash('Please Enter a Valid Email', category='error')
        elif len(firstname) <= 2:
            flash('Please Enter a Valid First Name', category='error')
        elif len(lastname) <= 2:
            flash('Please Enter a Valid Last Name', category='error')
        elif password1 != password2:
            flash('Password Do not Match', category='error')
        elif len(password1) <= 7:
            flash('Password must be 8 to 16 Characters', category='error')
        else:
            new_user = User(email=email, first_name=firstname, last_name=lastname,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account Created', category='success')
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)
