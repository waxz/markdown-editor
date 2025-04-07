import functools , flask ,urllib.parse
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('mdeditor', __name__,
    template_folder='dist',
    static_folder='dist/assets', static_url_path='/assets'
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


@bp.get("/")
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
