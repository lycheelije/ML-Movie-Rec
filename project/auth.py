"""Routes for user authentication."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_user
import flask_bcrypt
# from forms import LoginForm, SignupForm
# from app import login_manager, db, auth_bp


from project.app import login_manager, db
from project.forms import LoginForm, SignupForm
# from project.models import User
from project.libs.User import User

# Blueprint Configuration
auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)



@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    registerForm = SignupForm(request.form)
    current_app.logger.info(request.form)

    if request.method == 'POST' and registerForm.validate() == False:
        current_app.logger.info(registerForm.errors)
        return ("uhoh registration error")
    elif request.method == 'POST' and registerForm.validate():
        email = request.form['email']
		
        # generate password hash
        password_hash = flask_bcrypt.generate_password_hash(request.form['password']) #request.form['password']

        # prepare User
        user = User(email,password_hash)
        print (user)

        try:
            user.save()
            if login_user(user, remember="no"):
                flash("Logged in!")
                return redirect('/')
            else:
                flash("unable to log you in")

        except:
            flash("unable to register with that email address")
            current_app.logger.error("Error on registration - possible duplicate emails")

    templateData = {
		'form' : registerForm
	}

    return render_template("/register.html", **templateData)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        userObj = User()
        user = userObj.get_by_email_w_password(email)
        if user and flask_bcrypt.check_password_hash(user.password,request.form["password"]) and user.is_active():
            remember = request.form.get("remember", "no") == "yes"

            if login_user(user, remember=remember):
                flash("Logged in!")
                return redirect('/notes/create')
            else:
                flash("unable to log you in")

    return render_template("/login.html")


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth_bp.login"))