from flask import Flask, render_template, redirect, session 
from flask_debugtoolbar import DebugToolbarExtension
from models import User, connect_db, db
from forms import RegisterUserForm, LoginForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "abc123"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def redirect_to_register():
    """ Redirects to register page """

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    """ Show register form or handle registering of users. """

    form = RegisterUserForm()

    if form.validate_on_submit():
        
        username = form.username.data
        password = form.password.data

        new_user = User.register(username, password)

        new_user.email = form.email.data
        new_user.first_name = form.first_name.data
        new_user.last_name = form.last_name.data

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.username
        
        return redirect('/secret')

    else:
        return render_template(
            "register_user.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """ Show login form or handle login """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad username or password"]
        
    return render_template('login_user.html', form=form)


@app.route('/users/<username>')
def secret_page(username):
    """ Displays secret page if user is logged in """

    user = User.query.get(username)

    return render_template('user.html', username=user.username,
                                        email=user.email,
                                        first_name=user.first_name,
                                        last_name=user.last_name)


@app.route('/logout')
def logout_user():
    """ Logs user out of session and redirects to home page. """

    session.pop("user_id")

    return redirect("/")
