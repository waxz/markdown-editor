import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import hashlib

# Dummy database of users
PSW_FILE="./psw.d"

PSW_DATA = open(PSW_FILE)
PSW_DATA =  [l.strip() for l in PSW_DATA]

#####

bp = Blueprint('auth', __name__,
    #url_prefix = "/auth",
    template_folder='templates',
    static_folder='static', static_url_path='/assets/auth'
)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user_id

@bp.route('/login', methods=('GET', 'POST'))
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

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

