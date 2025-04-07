import functools
import flask,  urllib.parse
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import hashlib

import json
import os
from pathlib import Path

# Get environment variables.
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0")
VITE_ORIGIN = os.getenv("VITE_ORIGIN", "http://localhost:8101")

# Set application constants.
is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
is_production = FLASK_DEBUG != "1" or is_gunicorn
project_path = Path(os.path.dirname(os.path.abspath(__file__)))



# Dummy database of users
PSW_FILE = "./psw.d"
try:
    with open(PSW_FILE) as f:
        PSW_DATA = [line.strip() for line in f]
except FileNotFoundError:
    PSW_DATA = []
    print("Warning: Password file not found.")





#####

bp = Blueprint('auth', __name__,
    #url_prefix = "/auth",
    template_folder='templates',
    static_folder='static', static_url_path='/md/assets/auth'
)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user_id

@bp.route('/md/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")       
        user_psw = f"{username}:{password}"
        psw = hashlib.sha256(user_psw.encode('utf8')).digest().hex()
        
        print(f"username : {username}, password : {password}, psw ; {psw}")
        # Check credentials (you'll replace this with your own logic)
        if psw in PSW_DATA:
            session['logged_in'] = True
            session['user_id'] = username
            return redirect(url_for("mdeditor.index"))
        else:
            flash('Wrong username or password')
            #return 'Invalid username/password combination'
    return render_template('login.html')

@bp.route('/md/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# Add `asset()` function and `is_production` to app context.
@bp.context_processor
def add_context():
    print(f"hostname")
    
    def dev_asset(file_path):
        base_url = flask.request.base_url
        hostname = str(urllib.parse.urlparse(base_url).hostname)        
        print(f"dev_assets:{base_url} {hostname}")
        return f"/md/assets/auth/{file_path}"


    return {
        "asset": dev_asset,
        "is_production":is_production,
    }


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
