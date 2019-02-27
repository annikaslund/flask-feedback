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

    feedback = db.relationship('Feedback', backref='user')
     
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

    @classmethod
    def authenticate(cls, username, pwd):
        """ Validate that user exists and password is correct """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

    # def authorize(cls, username):
    # searched_user = User.query.get(username)
    # user_id = session.get('user_id')

    # if 

    # @classmethod
    # def check_if_email_exists(cls, email):
    #     ''' verifies if email is unique'''
    #     email_in_db = User.query.filter_by(email=email).first()

    #     return email_in_db

    # @classmethod
    # def check_if_username_exists(cls, username):
    #     ''' verifies if username is unique'''
    #     username_in_db = User.query.filter_by(username=username).first()

    #     return username_in_db


class Feedback(db.Model):
    ''' Feedback class from users '''

    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   )

    title = db.Column(db.String(100),
                      nullable=False,
                      )

    content = db.Column(db.Text,
                        nullable=False,
                        )

    username = db.Column(db.String(20),
                         db.ForeignKey('users.username'),
                         nullable=False,
                         )
