from flask import Flask, redirect, url_for
from flask import Flask as flask, request, jsonify

from flask_session import Session
from flask_protobuf import flask_protobuf as FlaskProtobuf
import os


from auth import auth
from mdeditor import mdeditor


from api.employees_pb2 import Employees as employees

FLASK_BASE_URL = os.getenv("FLASK_BASE_URL", "mde")


print(f"FLASK_BASE_URL: {FLASK_BASE_URL}")
# Dummy database of users
PSW_FILE = "./psw.d"

PSW_DATA = open(PSW_FILE)
PSW_DATA = [line.strip() for line in PSW_DATA]

# Set up application.
app = Flask(
    __name__,
    static_url_path=f"/{FLASK_BASE_URL}",
    static_folder="public",
    template_folder="templates",
)
sess = Session()
app.secret_key = "super secret key"
app.config["SESSION_TYPE"] = "filesystem"
sess.init_app(app)

# Provide Vite context processors and static assets directory.
app.register_blueprint(
    mdeditor.bp,
)
app.register_blueprint(auth.bp)


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("auth.login"))


# declare FlaskProtobuf
fb = FlaskProtobuf(app, parse_dict=True)


@app.route("/get-employee", methods=["POST"])
@fb(employees)
def index():
    print(233)
    employees_array = request.data
    for employee in employees_array:
        print(employee)

    return jsonify({"status": "SUCCESS"})


if __name__ == "__main__":
    # Normal entry point
    app.run()
