from flask import Flask, render_template, redirect, session 
from flask_debugtoolbar import DebugToolbarExtension
from models import User, connect_db, db
from forms import RegisterUserForm


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
    """ Show register form, handles registering of users. """

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

        session['user_id'] = new_user.id
        
        return redirect('/secret')

    else:
        return render_template(
            "register_user.html", form=form)