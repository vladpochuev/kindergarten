import os
from os.path import join, dirname

import psycopg2
from dotenv import load_dotenv


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
