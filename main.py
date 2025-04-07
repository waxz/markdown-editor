from flask import Flask, render_template, g, session, request, redirect, url_for, flash

import flask,  urllib.parse
from flask_session import Session
import hashlib
import argparse
import sys, os


from  auth import auth
from mdeditor import mdeditor

FLASK_BASE_URL = os.getenv("FLASK_BASE_URL", "mde")


print(f"FLASK_BASE_URL: {FLASK_BASE_URL}")
# Dummy database of users
PSW_FILE="./psw.d"

PSW_DATA = open(PSW_FILE)
PSW_DATA =  [l.strip() for l in PSW_DATA]

# Set up application.
app = Flask(
        __name__,
        static_url_path=f"/{FLASK_BASE_URL}",
        static_folder="public",
        template_folder="templates",
)
sess = Session()
app.secret_key = 'super secret key' 
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)

# Provide Vite context processors and static assets directory.
app.register_blueprint(mdeditor.bp, )
app.register_blueprint(auth.bp)

if __name__ == "__main__":
    # Normal entry point
    app.run()
