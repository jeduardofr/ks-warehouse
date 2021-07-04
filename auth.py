import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from database import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

def no_session(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user:
            return redirect(url_for("project.index"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE id = %s", [user_id]).fetchone()
        )

@bp.route("/login", methods=["GET", "POST"])
@no_session
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM users WHERE email = %s", [email]
        ).fetchone()

        if user is None or not check_password_hash(user["password"], password):
            error = "Correo electrónico o contraseña inválido"

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("project.index"))

        flash(error)

    return render_template("views/auth/login.html")


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return {}
