import os
import random
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'my_super_secret_CODE_eveR'
app.config['UPLOAD_FOLDER'] = 'static/files'
manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload")


class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    ingredient = db.Column(db.String(20), nullable=False)
    image_name = db.Column(db.String(50), nullable=False)


class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DATE, default=datetime.today().date())


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    all_recipe = Recipes.query.all()
    info_count = len(all_recipe)
    all_breakfasts = Recipes.query.filter_by(type='breakfast').all()
    breakfasts_count = len(all_breakfasts)
    all_lunches = Recipes.query.filter_by(type='lunch').all()
    lunches_count = len(all_lunches)
    all_desserts = Recipes.query.filter_by(type='dessert').all()
    desserts_count = len(all_desserts)
    all_grills = Recipes.query.filter_by(type='grill').all()
    grills_count = len(all_grills)

    return render_template('dashboard.html', info_count=info_count, breakfasts_count=breakfasts_count,
                           lunches_count=lunches_count, desserts_count=desserts_count, grills_count=grills_count)


@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        image_type = os.path.splitext(file.filename)
        image_name = str(random.uniform(12345, 9999999)) + image_type[1]
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'], secure_filename(image_name)))
        recipe_name = request.form.get('recipe_name')
        recipe_description = request.form.get('recipe_description')
        recipe_type = request.form.get('recipe_type')
        recipe_ingredient = request.form.get('recipe_ingredient').lower()
        recipe_image = image_name
        recipe = Recipes(name=recipe_name, description=recipe_description, type=recipe_type,
                         ingredient=recipe_ingredient, image_name=recipe_image)
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('add_recipe.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page)
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('login.html')


@app.route('/register-new-user', methods=['GET', 'POST'])
@login_required
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response


@app.route('/success')
@login_required
def success():
    return render_template('success.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005)
