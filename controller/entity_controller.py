from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_required, current_user

from mapper import *
from service import *

entity_blueprint = Blueprint("entity", __name__)


def get_child_dto(child, db):
    group = db.groups.get_by_id(child.group_id)
    educator = db.educators.get_by_id(group.educator_id)
    parent = db.parents.get_by_id(child.parent_id)
    menu = db.menus.get_by_id(child.menu_id)

    return ChildDTOMapper().from_entity(child, group, educator, parent, menu)


@entity_blueprint.route("/", methods=["GET"])
@handle_connection
def get_children(db):
    children_dto_list = []
    for child in db.children.get_all():
        child_dto = get_child_dto(child, db)
        children_dto_list.append(child_dto)

    return render_template("children.html", children=children_dto_list)


@entity_blueprint.route("/parent/<parent_id>", methods=["GET"])
@handle_connection
def get_parent(db, parent_id):
    parent = db.parents.get_by_id(parent_id)
    parent_dto = ParentDTOMapper().from_entity(parent)
    return render_template("parent.html", parent=parent_dto)


@entity_blueprint.route("/group/<group_id>", methods=["GET"])
@handle_connection
def get_group(db, group_id):
    group = db.groups.get_by_id(group_id)
    educator = db.educators.get_by_id(group.educator_id)
    children = db.children.get_by_group(group_id)

    group_dto = GroupDTOMapper().from_entity(group, educator, children)
    return render_template("group.html", group=group_dto)


@entity_blueprint.route("/educator/<educator_id>", methods=["GET"])
@handle_connection
def get_educator(db, educator_id):
    educator = db.educators.get_by_id(educator_id)
    educator_dto = EducatorDTOMapper().from_entity(educator)
    return render_template("educator.html", educator=educator_dto)


@entity_blueprint.route("/menu/<menu_id>", methods=["GET"])
@handle_connection
def get_menu(db, menu_id):
    menu = db.menus.get_by_id(menu_id)
    menu_dto = MenuDTOMapper().from_entity(menu)
    return render_template("menu.html", menu=menu_dto)


def get_menu_list_dto(db):
    menu_list_dto = []
    for menu in db.menus.get_all():
        menu_dto = MenuDTOMapper().from_entity(menu)
        menu_list_dto.append(menu_dto)
    return menu_list_dto


def get_group_dto(group, db):
    educator = db.educators.get_by_id(group.educator_id)
    children = db.children.get_by_group(group.id)
    return GroupDTOMapper().from_entity(group, educator, children)


def get_groups_dto(db):
    groups_dto = []
    for group in db.groups.get_all():
        group_dto = get_group_dto(group, db)
        groups_dto.append(group_dto)
    return groups_dto


@entity_blueprint.route("/new_child", methods=["GET"])
@login_required
@handle_connection
def get_new_child(db):
    groups_dto = get_groups_dto(db)
    menu_list_dto = get_menu_list_dto(db)
    return render_template("new-child.html", menu_list=menu_list_dto, groups=groups_dto)


def is_age_suitable(new_child, group):
    birth_date = get_date_from_string(new_child.birth_date)
    child_age = get_age(birth_date)
    return not group.from_age <= child_age <= group.to_age


@entity_blueprint.route("/new_child", methods=["POST"])
@login_required
@handle_connection
def post_new_child(db):
    new_child = NewChildFormExtractor(request.form).get_new_child()
    parent = db.parents.get_by_name(current_user.username)
    group = db.groups.get_by_id(new_child.group_id)

    if is_age_suitable(new_child, group):
        flash("Дитина не відповідає віковим вимогам цієї групи")
        return redirect(url_for("entity.get_new_child"))

    try:
        child = ChildDTOMapper().to_entity(new_child, parent.id)
        db.children.save(child)
    except ValueError:
        flash("Помилка реєстрації дитини")
        return redirect(url_for("entity.get_new_child"))

    flash("Дитина успішно додана")
    return redirect(url_for("entity.get_children"))
