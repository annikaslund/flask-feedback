from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import User, connect_db, db
# from forms import 


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


@app.route('/register')
def register_user():
    """ Show register form, handles registering of users. """

    form = AddSnackForm()

    if form.validate_on_submit():
        # import pdb
        # pdb.set_trace()
        name = form.name.data
        price = form.price.data
        return f"Add {name} at {price}"
        # redirect("/")

    else:
        return render_template(
            "snack_add_form.html", form=form)