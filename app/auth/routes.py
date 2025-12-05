# -------------------------------------------------------------
# Authentication Routes (Login + Logout)
# -------------------------------------------------------------

from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    request,
)
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required,
)

from ..forms import LoginForm
from ..models import User

# Blueprint for authentication routes
auth_bp = Blueprint("auth", __name__, template_folder="templates")


# -------------------------------------------------------------
# LOGIN ROUTE
# -------------------------------------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Already logged in? → send to home/dashboard
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    # When login form is submitted
    if form.validate_on_submit():
        # Look up user
        user = User.query.filter_by(username=form.username.data).first()

        # Invalid username or password
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.", "danger")
            return redirect(url_for("auth.login"))

        # Login user
        remember_flag = False
        if hasattr(form, "remember_me"):
            remember_flag = form.remember_me.data

        login_user(user, remember=remember_flag)

        # Redirect to next page or homepage
        next_page = request.args.get("next")
        if not next_page or not next_page.startswith("/"):
            next_page = url_for("main.index")

        return redirect(next_page)

    # GET request or failed login → show login page
    return render_template("auth/login.html", form=form)


# -------------------------------------------------------------
# LOGOUT ROUTE
# -------------------------------------------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

