from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import User, connect_db, db
# from forms import 


app = Flask(__name__)

app.config["SECRET_KEY"] = "abc123"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///adoption_agency"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)