from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from dao import *
from mappers import *
from system_utils import *

app = Flask(__name__, template_folder="templates")
app.secret_key = get_from_env("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    parent_dao = ParentDAO(conn)

    return parent_dao.get_by_id(user_id)


@app.route("/")
def main_controller():
    conn = get_db_connection()

    children_dao = ChildDAO(conn)
    parent_dao = ParentDAO(conn)
    educator_dao = EducatorDAO(conn)
    group_dao = GroupDAO(conn)
    menu_dao = MenuDAO(conn)

    children_dao_list = []
    children = children_dao.get_all()
    for child in children:
        group = group_dao.get_by_id(child.group_id)
        educator = educator_dao.get_by_id(group.educator_id)
        parent = parent_dao.get_by_id(child.parent_contact_id)
        menu = menu_dao.get_by_id(child.menu_id)

        child_dto = get_child_dto(child, group, educator, parent, menu)
        children_dao_list.append(child_dto)

    conn.close()
    return render_template("children.html", children=children_dao_list)


@app.route("/parent/<parent_id>")
def parent_controller(parent_id):
    conn = get_db_connection()

    parent_dao = ParentDAO(conn)
    parent = parent_dao.get_by_id(parent_id)
    parent_dto = get_parent_dto(parent)

    conn.close()
    return render_template("parent.html", parent=parent_dto)


@app.route("/group/<group_id>")
def group_controller(group_id):
    conn = get_db_connection()

    group_dao = GroupDAO(conn)
    educator_dao = EducatorDAO(conn)
    children_dao = ChildDAO(conn)

    group = group_dao.get_by_id(group_id)
    educator = educator_dao.get_by_id(group.educator_id)
    children = children_dao.get_by_group(group_id)

    group_dto = get_group_dto(group, educator, children)

    conn.close()
    return render_template("group.html", group=group_dto)


@app.route("/educator/<educator_id>")
def educator_controller(educator_id):
    conn = get_db_connection()

    educator_dao = EducatorDAO(conn)
    educator = educator_dao.get_by_id(educator_id)
    educator_dto = get_educator_dto(educator)

    conn.close()
    return render_template("educator.html", educator=educator_dto)


@app.route("/menu/<menu_id>")
def menu_controller(menu_id):
    conn = get_db_connection()

    menu_dao = MenuDAO(conn)
    menu = menu_dao.get_by_id(menu_id)
    menu_dto = get_menu_dto(menu)

    conn.close()
    return render_template("menu.html", menu=menu_dto)


@app.route('/register', methods=['POST'])
def register_post():
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
        return redirect(url_for('register_get'))

    password_hash = generate_password_hash(password)
    parent_dao.save(Parent(None, first_name, last_name, birth_date, phone_number, email, gender, password_hash))
    return redirect(url_for('login_get'))


@app.route('/register', methods=['GET'])
def register_get():
    return render_template("register.html", title="Register")


@app.route('/login', methods=['POST'])
def login_post():
    conn = get_db_connection()
    parent_dao = ParentDAO(conn)

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']

    parent = parent_dao.get_by_name(first_name + " " + last_name)
    if parent and parent.verify_password(password):
        login_user(parent)
        return redirect(url_for('main_controller'))
    return redirect(url_for('login_get'))


@app.route('/login', methods=['GET'])
def login_get():
    return render_template("login.html", title="Login")


@login_required
@app.route('/logout', methods=['POST'])
def logout_post():
    logout_user()
    return redirect(url_for('main_controller'))


@login_required
@app.route('/logout', methods=['GET'])
def logout_get():
    return render_template('logout.html', title="Logout")


if __name__ == "__main__":
    app.run()
