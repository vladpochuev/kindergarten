from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from mapper import *
from service import *

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["GET"])
def get_register():
    return render_template("authentication/register.html", title="Register")


def is_user_exists(register, db):
    full_name = register.first_name + " " + register.last_name
    return db.parents.exists_by_name(full_name)


def save_new_user(register, db):
    password_hash = generate_password_hash(register.password)
    parent = ParentDTOMapper().to_entity(register, password_hash)
    db.parents.save(parent)


@auth_blueprint.route("/register", methods=["POST"])
@handle_connection
def post_register(db):
    register = RegisterFormExtractor(request.form).get_register()

    if is_user_exists(register, db):
        flash("Користувач із таким іменем уже існує")
        return redirect(url_for("auth.get_register"))

    save_new_user(register, db)
    flash("Реєстрація успішна. Будь ласка, увійдіть до акаунту")
    return redirect(url_for("auth.get_login"))


@auth_blueprint.route("/login", methods=["GET"])
def get_login():
    return render_template("authentication/login.html", title="Login")


def get_user(login, db):
    full_name = login.first_name + " " + login.last_name
    return db.parents.get_by_name(full_name)


@auth_blueprint.route("/login", methods=["POST"])
@handle_connection
def post_login(db):
    login = LoginFormExtractor(request.form).get_login()
    user = get_user(login, db)

    if not (user and user.verify_password(login.password)):
        flash("Неправильне ім'я або пароль")
        return redirect(url_for("auth.get_login"))

    login_user(user)
    flash("Вхід успішний")
    return redirect(url_for("entity.get_children"))


@auth_blueprint.route("/logout", methods=["GET"])
@login_required
def get_logout():
    return render_template("authentication/logout.html", title="Logout")


@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def post_logout():
    logout_user()
    flash("Ви успішно вийшли з акаунту")
    return redirect(url_for("entity.get_children"))
