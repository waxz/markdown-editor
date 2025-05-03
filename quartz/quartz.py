from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify
)

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
FLASK_BASE_URL = os.getenv("FLASK_BASE_URL", "mde")
print(f"FLASK_BASE_URL: {FLASK_BASE_URL}")

FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0")

# Set application constants.
is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
is_production = FLASK_DEBUG != "1" or is_gunicorn
project_path = Path(os.path.dirname(os.path.abspath(__file__)))

bp = Blueprint('quartz', __name__,
    template_folder='../templates',
    static_folder='../templates/quartz-dist', static_url_path=f'/{FLASK_BASE_URL}/assets/quartz'
)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user_id


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.get(f"/{FLASK_BASE_URL}/quartz", strict_slashes=False)
def index():
    if not 'logged_in' in session:
        return redirect(url_for('auth.login'))

    base_url = flask.request.base_url
    hostname = str(urllib.parse.urlparse(base_url).hostname)
    session["base_url"] = base_url
    session["hostname"] = hostname

    msg =  f"base_url:{base_url}, hostname:{hostname}"
    print("quartz recieve request url: ", msg)
    html = render_template("./quartz-dist/index.html")
    # print(html)
    
    return html
@bp.get(f"/{FLASK_BASE_URL}/quartz/<path:filepath>")
def file_index(filepath):
    # return filepath;

    if not 'logged_in' in session:
        return redirect(url_for('auth.login'))

    base_url = flask.request.base_url
    hostname = str(urllib.parse.urlparse(base_url).hostname)
    session["base_url"] = base_url
    session["hostname"] = hostname

    msg =  f"base_url:{base_url}, hostname:{hostname}"
    print("quartz recieve request url: ", msg)
    
    try:
        # Try rendering the template from the quartz-dist folder
        template_path = f"./quartz-dist/{filepath}/index.html"
        html = render_template(template_path)
    except Exception as e:
        # If the above fails, try looking for the template as a .html file
        print(f"Error rendering template: {e}")
        template_path = f"./quartz-dist/{filepath}.html"
        try:
            html = render_template(template_path)
        except Exception as e:
            print(f"Error rendering alternative template: {e}")
            return f"Template not found: {filepath}", 404  # Return a 404 error if both fail

    return html
    
# Add `asset()` function and `is_production` to app context.
@bp.context_processor
def add_context():
    
    def dev_asset(file_path):
        base_url = flask.request.base_url
        hostname = str(urllib.parse.urlparse(base_url).hostname)        
        print(f"quartz dev_assets:{base_url} {hostname}")
        return f"/{FLASK_BASE_URL}/assets/quartz/{file_path}"


    return {
        "asset": dev_asset,
        "is_production":is_production,
    }