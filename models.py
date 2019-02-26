from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """ Connects to database. """
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User model """
     
    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True,)
   
    password = db.Column(db.Text,
                         nullable=False,)
  
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True,)
    
    first_name = db.Column(db.String(30),
                           nullable=False,)

    last_name = db.Column(db.String(30),
                          nullable=False,)

    @classmethod
    def register(cls, username, pwd):
        """ Returns instance of user with username and encrypted password """
        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8)