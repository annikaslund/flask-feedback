from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Feedback, connect_db, db
from forms import RegisterUserForm, LoginForm, AddFeedbackForm, EditFeedbackForm


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
        
        return redirect(f'/users/{new_user.username}')

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
    searched_user = User.query.get(username)
    user_id = session.get('user_id')
    
    if searched_user is None or user_id != searched_user.username:
        flash(f"You must be logged in as {username} to view!")
        return redirect("/login")

    return render_template('user.html',
                           username=searched_user.username,
                           email=searched_user.email,
                           first_name=searched_user.first_name,
                           last_name=searched_user.last_name,
                           feedback_list=searched_user.feedback)


@app.route('/logout')
def logout_user():
    """ Logs user out of session and redirects to home page. """

    session.pop("user_id")

    return redirect("/")


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    ''' deletes user from db'''
    searched_user = User.query.get(username)
    user_id = session.get('user_id')

    if searched_user is None or user_id != searched_user.username:
        flash(f"You must be logged in as {username} to view!")
        return redirect("/login")

    user_to_delete = User.query.get(username)
    
    db.session.delete(user_to_delete)
    db.session.commit()

    flash(f'User {username} has successfully been deleted.')
    return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def new_feedback_form(username):

    searched_user = User.query.get(username)
    user_id = session.get('user_id')

    if searched_user is None or user_id != searched_user.username:
        flash(f"You must be logged in as {username} to view!")
        return redirect("/login")
    
    form = AddFeedbackForm()

    if form.validate_on_submit():
        
        title = form.title.data
        content = form.content.data
        username_key = username

        new_feedback = Feedback(title=title, content=content, username=username_key)

        db.session.add(new_feedback)
        db.session.commit()
        
        return redirect(f'/users/{username}')

    else:
        return render_template(
            "add_feedback.html", form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def edit_feedback(feedback_id):
    """ Edit specified feedback """

    post = Feedback.query.get_or_404(feedback_id)
    searched_user = post.user

    user_id = session.get('user_id')

    if searched_user is None or user_id != searched_user.username:
        flash(f"You must be logged in as {searched_user.username} to view!")
        return redirect("/login")

    form = EditFeedbackForm(obj=post)

    if form.validate_on_submit():
        
        post.title = form.title.data
        post.content = form.content.data

        db.session.commit()
        
        return redirect(f'/users/{searched_user.username}')

    else:
        return render_template(
            "edit_feedback.html", form=form)

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    
    post = Feedback.query.get_or_404(feedback_id)
    searched_user = post.user

    user_id = session.get('user_id')

    if searched_user is None or user_id != searched_user.username:
        flash(f"You must be logged in as {searched_user.username} to view!")
        return redirect("/login")

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{searched_user.username}')
