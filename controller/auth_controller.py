from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from dao import *
from model import *
from service import *

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['GET'])
def get_register():
    return render_template("authentication/register.html", title="Register")


@auth_blueprint.route('/register', methods=['POST'])
def post_register():
    conn = get_db_connection()
    parent_dao = ParentDAO(conn)

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    birth_date = request.form['birth_date']
    phone_number = request.form['phone_number']
    email = request.form['email']
    gender = request.form['gender']
    password = request.form['password']

    if parent_dao.exists_by_name(first_name + ' ' + last_name):
        flash('Username already exists.')
        conn.close()
        return redirect(url_for('auth.get_register'))

    password_hash = generate_password_hash(password)
    parent_dao.save(Parent(None, first_name, last_name, birth_date, phone_number, email, gender, password_hash))
    flash('Registration successful. Please log in.')
    conn.close()
    return redirect(url_for('auth.get_login'))


@auth_blueprint.route('/login', methods=['GET'])
def get_login():
    return render_template("authentication/login.html", title="Login")


@auth_blueprint.route('/login', methods=['POST'])
def post_login():
    conn = get_db_connection()
    parent_dao = ParentDAO(conn)

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']

    parent = parent_dao.get_by_name(first_name + " " + last_name)
    if parent and parent.verify_password(password):
        login_user(parent)
        flash('Login successful!')
        conn.close()
        return redirect(url_for('entity.get_children'))
    flash('Invalid username or password.')
    conn.close()
    return redirect(url_for('auth.get_login'))


@auth_blueprint.route('/logout', methods=['GET'])
@login_required
def get_logout():
    return render_template('authentication/logout.html', title="Logout")


@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def post_logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('entity.get_children'))
