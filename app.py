from os.path import join, dirname

from flask import Flask
from flask_login import LoginManager

from src.python.controller import auth_blueprint, entity_blueprint
from src.python.service import set_dotenv, get_from_env, handle_connection

dotenv_path = join(dirname(__file__), ".env")
set_dotenv(dotenv_path)

app = Flask(__name__, template_folder="src/resources/templates", static_folder="src/resources/static")
app.secret_key = get_from_env("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.get_login"

app.register_blueprint(auth_blueprint)
app.register_blueprint(entity_blueprint)


@login_manager.user_loader
@handle_connection
def load_user(db, user_id):
    return db.parents.get_by_id(user_id)


if __name__ == "__main__":
    app.run()
