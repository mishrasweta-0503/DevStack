from flask import Flask, render_template, request,redirect,url_for,flash
from models import db, User, Resource
from forms import RegistrationForm,LoginForm,ResourceForm
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

db_path = os.path.join(basedir, 'instance', 'project.db')

#configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to suppress warning
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') #this key is needed for forms later



db.init_app(app) #This "plugs" the database setup from models.py into this specific app.

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' #Tells it where to go if access is denied

#The user_loader is the function that tells Flask-Login: "Whenever you see this ID coming from a cookie,
#  here is how you find the actual User object in our database."
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
@login_required
def home():
    search_term = request.args.get('search_term')
    category_term = request.args.get('category_term')
    query = Resource.query
    if search_term:
        query = query.filter(Resource.title.contains(search_term) | Resource.description.contains(search_term))
    if category_term and category_term != "":
        query = query.filter(Resource.category == category_term)
    resources = query.all()
    return render_template('home.html', resources=resources)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return(redirect(url_for('home')))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return(redirect(url_for('home'))) #this creates a session
        else:
            print(f"Login failed for {user.username}. Check email and password.")   
    return render_template('login.html',form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) |
            (User.email == form.email.data)
        ).first()
        if existing_user:
            flash('Username or email already exists. Please try another one.', 'danger')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data, 
            email=form.email.data, 
            password_hash=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/add_resource', methods=['GET', 'POST'])
@login_required
def add_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        new_resource = Resource(
            title = form.title.data,
            description = form.description.data,
            url = form.url.data,
            category = form.category.data,
            user_id=current_user.id
        )
        db.session.add(new_resource)
        db.session.commit()
        print("Resource successfully saved to the database!")
        return redirect(url_for('home'))
    return render_template('add_resource.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    print("User logged out.")
    return redirect(url_for('login'))

@app.route('/delete/<int:resource_id>',methods=['POST'])
@login_required
def delete_resources(resource_id):
    resource_to_delete = Resource.query.get_or_404(resource_id)
    if resource_to_delete.user_id == current_user.id:
        db.session.delete(resource_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    return redirect(url_for('home'))


with app.app_context():
    db.create_all()