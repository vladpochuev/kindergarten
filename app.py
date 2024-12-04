from flask import Flask, render_template

import os
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
import psycopg2

from ChildDTO import ChildDTO
from ParentDTO import ParentDTO
from dao import *

app = Flask(__name__)


def get_from_env(key):
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    return os.environ.get(key)


def get_db_connection():
    conn = psycopg2.connect(host="localhost",
                            database=get_from_env("DB_NAME"),
                            user=get_from_env("DB_USER"),
                            password=get_from_env("DB_PASSWORD"))
    return conn


def get_age(birth_date):
    today = datetime.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


@app.route('/')
def main():
    conn = get_db_connection()

    children_dao = ChildrenDAO(conn)
    parent_dao = ParentDAO(conn)
    educator_dao = EducatorDAO(conn)
    group_dao = GroupDAO(conn)
    menu_dao = MenuDAO(conn)

    children = children_dao.get_all()
    children_dao_list = []
    for child in children:
        group = group_dao.get_by_id(child[5])
        educator = educator_dao.get_by_id(group[1])
        parent = parent_dao.get_by_id(child[6])
        menu = menu_dao.get_by_id(child[7])

        birth_date = child[3]
        age = get_age(birth_date)

        children_dto = ChildDTO(child[1], child[2], age, child[4], parent[0], parent[1] + " " + parent[2],
                                group[2],
                                educator[1] + " " + educator[2], menu[2])
        children_dao_list.append(children_dto)

    conn.close()
    return render_template("index.html", children=children_dao_list)


@app.route('/parent/<parent_id>')
def parent(parent_id):
    conn = get_db_connection()
    parent_dao = ParentDAO(conn)
    parent = parent_dao.get_by_id(parent_id)
    parent_dto = ParentDTO(parent[1] + " " + parent[2], get_age(parent[3]), parent[6], parent[4], parent[5])

    return render_template("parent.html", parent=parent_dto)


if __name__ == '__main__':
    app.run()
