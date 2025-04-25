from flask import Flask, redirect, url_for
from flask import Flask as flask, request, jsonify

from flask_session import Session
from flask_protobuf import flask_protobuf as FlaskProtobuf
import os
# from flask_sockets import Sockets
import time
import logging
from flask_cors import CORS

from flask_socketio import SocketIO, send

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




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

CORS(app)

socketio = SocketIO(app, path=f'/{FLASK_BASE_URL}/socket.io')

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("auth.login"))


# declare FlaskProtobuf
fb = FlaskProtobuf(app, parse_dict=True)


@app.route(f'/{FLASK_BASE_URL}/')
def index():
    """Serves a simple message indicating the server is running."""
    return "Protobuf WebSocket Server is running. Connect via WebSocket client.", 200


@socketio.on('message')
def handle_message(msg):
    print('Received message:', msg)
    send(f"Echo: {msg}", broadcast=True)

if __name__ == "__main__":
    # Normal entry pointd
    app.run()
    # socketio.run(app)