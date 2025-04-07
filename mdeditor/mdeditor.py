import functools , flask ,urllib.parse
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
VITE_ORIGIN = os.getenv("VITE_ORIGIN", "http://localhost:8101")


# Set application constants.
is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
is_production = FLASK_DEBUG != "1" or is_gunicorn
project_path = Path(os.path.dirname(os.path.abspath(__file__)))





bp = Blueprint('mdeditor', __name__,
    template_folder='dist',
    static_folder='dist/assets', static_url_path=f'/{FLASK_BASE_URL}/assets'
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


@bp.get(f"/{FLASK_BASE_URL}/editor")
def index():
    if not 'logged_in' in session:
        return redirect(url_for('auth.login'))

    base_url = flask.request.base_url
    hostname = str(urllib.parse.urlparse(base_url).hostname)
    session["base_url"] = base_url
    session["hostname"] = hostname

    msg =  f"base_url:{base_url}, hostname:{hostname}"
    print("msg: ", msg)
    return render_template("index.html")
    
# Add `asset()` function and `is_production` to app context.
@bp.context_processor
def add_context():
    print(f"hostname")
    
    def dev_asset(file_path):
        base_url = flask.request.base_url
        hostname = str(urllib.parse.urlparse(base_url).hostname)        
        print(f"dev_assets:{base_url} {hostname}")
        return f"/{FLASK_BASE_URL}/assets/{file_path}"


    return {
        "asset": dev_asset,
        "is_production":is_production,
    }

@bp.route(f"/{FLASK_BASE_URL}/editor/md/save", methods=["POST"])
def save_markdown():
    user_id = session['user_id']
    data = request.get_json()
    markdown = data.get("markdown", "")

    filename = data.get("filename", "untitled").strip()

    if not filename:
        filename = "untitled"

    if not filename.endswith(".md"):
        filename += ".md"

    safe_name = filename.replace("/", "_")  # avoid path traversal
    if not markdown:
        return jsonify({"message": "No markdown received"}), 400

    # Save to file, DB, or wherever you want
    with open(f"saved/{safe_name}", "w", encoding="utf-8") as f:
        f.write(markdown)

    return jsonify({"message": "Markdown saved successfully!"})
