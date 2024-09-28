from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from blogspot.models import User, BlogPost  # Import models after initializing the app

# Routes go here...

if __name__ == "__main__":
    app.run(debug=True)
from flask import render_template, redirect, flash, url_for
from blogspot.models import User, BlogPost
from blogspot.forms import RegistrationForm, LoginForm, PostForm
from blogspot.app import app, db
from flask_login import login_user, current_user, logout_user, login_required

# Home page showing all blog posts
@app.route('/')
def home():
    posts = BlogPost.query.all()
    return render_template('home.html', posts=posts)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Login unsuccessful. Please check your credentials.', 'danger')
    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Route to create a new blog post
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = BlogPost(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form)

# Route to view a single post
@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)
