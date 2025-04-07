from flask import Flask, render_template, g, session, request, redirect, url_for, flash

import flask,  urllib.parse
from flask_session import Session
import hashlib


from  auth import auth
from mdeditor import mdeditor

# Dummy database of users
PSW_FILE="./psw.d"

PSW_DATA = open(PSW_FILE)
PSW_DATA =  [l.strip() for l in PSW_DATA]

# Set up application.
app = Flask(
    __name__,
    static_url_path="/",
    static_folder="public",
    template_folder="templates",
)
sess = Session()
app.secret_key = 'super secret key' 
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)

# Provide Vite context processors and static assets directory.
app.register_blueprint(mdeditor.bp, 
#url_prefix='/mde'

)
app.register_blueprint(auth.bp)



# Start the app if the file is run directly.
if __name__ == "__main__":
    app.run()
