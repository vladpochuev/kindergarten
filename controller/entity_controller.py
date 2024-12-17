from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_required, current_user

from dao import *
from mapper import *
from model import *
from service import *

entity_blueprint = Blueprint('entity', __name__)


@entity_blueprint.route("/", methods=["GET"])
def get_children():
    conn = get_db_connection()

    children_dao = ChildDAO(conn)
    parent_dao = ParentDAO(conn)
    educator_dao = EducatorDAO(conn)
    group_dao = GroupDAO(conn)
    menu_dao = MenuDAO(conn)

    children_dto_list = []
    children = children_dao.get_all()
    for child in children:
        group = group_dao.get_by_id(child.group_id)
        educator = educator_dao.get_by_id(group.educator_id)
        parent = parent_dao.get_by_id(child.parent_id)
        menu = menu_dao.get_by_id(child.menu_id)

        child_mapper = ChildMapper()
        child_dto = child_mapper.get_child_dto(child, group, educator, parent, menu)
        children_dto_list.append(child_dto)

    conn.close()
    return render_template("children.html", children=children_dto_list)


@entity_blueprint.route("/parent/<parent_id>", methods=["GET"])
def get_parent(parent_id):
    conn = get_db_connection()

    parent_dao = ParentDAO(conn)
    parent = parent_dao.get_by_id(parent_id)
    parent_mapper = ParentMapper()
    parent_dto = parent_mapper.get_parent_dto(parent)

    conn.close()
    return render_template("parent.html", parent=parent_dto)


@entity_blueprint.route("/group/<group_id>", methods=["GET"])
def get_group(group_id):
    conn = get_db_connection()

    group_dao = GroupDAO(conn)
    educator_dao = EducatorDAO(conn)
    children_dao = ChildDAO(conn)

    group = group_dao.get_by_id(group_id)
    educator = educator_dao.get_by_id(group.educator_id)
    children = children_dao.get_by_group(group_id)

    group_mapper = GroupMapper()
    group_dto = group_mapper.get_group_dto(group, educator, children)

    conn.close()
    return render_template("group.html", group=group_dto)


@entity_blueprint.route("/educator/<educator_id>", methods=["GET"])
def get_educator(educator_id):
    conn = get_db_connection()

    educator_dao = EducatorDAO(conn)
    educator = educator_dao.get_by_id(educator_id)
    educator_mapper = EducatorMapper()
    educator_dto = educator_mapper.get_educator_dto(educator)

    conn.close()
    return render_template("educator.html", educator=educator_dto)


@entity_blueprint.route("/menu/<menu_id>", methods=["GET"])
def get_menu(menu_id):
    conn = get_db_connection()

    menu_dao = MenuDAO(conn)
    menu = menu_dao.get_by_id(menu_id)
    menu_mapper = MenuMapper()
    menu_dto = menu_mapper.get_menu_dto(menu)

    conn.close()
    return render_template("menu.html", menu=menu_dto)


@entity_blueprint.route("/new_child", methods=["GET"])
@login_required
def get_new_child():
    conn = get_db_connection()
    group_dao = GroupDAO(conn)
    menu_dao = MenuDAO(conn)
    educator_dao = EducatorDAO(conn)
    child_dao = ChildDAO(conn)

    groups_dto = []
    groups = group_dao.get_all()
    for group in groups:
        educator = educator_dao.get_by_id(group.educator_id)
        children = child_dao.get_by_group(group.id)
        group_mapper = GroupMapper()
        groups_dto.append(group_mapper.get_group_dto(group, educator, children))

    menu_list_dto = []
    menu_list = menu_dao.get_all()
    for menu in menu_list:
        menu_mapper = MenuMapper()
        menu_list_dto.append(menu_mapper.get_menu_dto(menu))

    conn.close()
    return render_template("new-child.html", menu_list=menu_list_dto, groups=groups_dto)


@entity_blueprint.route("/new_child", methods=["POST"])
@login_required
def post_new_child():
    conn = get_db_connection()
    parent_dao = ParentDAO(conn)
    child_dao = ChildDAO(conn)
    group_dao = GroupDAO(conn)

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    birth_date = request.form['birth_date']
    gender = request.form['gender']
    group_id = request.form['group']
    menu_id = request.form['menu']
    parent = parent_dao.get_by_name(current_user.username)

    group = group_dao.get_by_id(group_id)
    child_age = get_age(get_date_from_string(birth_date))
    if child_age < group.from_age or child_age > group.to_age:
        flash("The child does not meet the age requirements for this group.")
        return redirect(url_for('entity.get_new_child'))

    try:
        child_dao.save(Child(None, first_name, last_name, birth_date, gender, group_id, parent.id, menu_id))
        flash("Child added successfully")
        conn.close()
        return redirect(url_for('entity.get_children'))
    except ValueError:
        flash("Error while creating new child")
        conn.close()
        return redirect(url_for('entity.get_new_child'))
