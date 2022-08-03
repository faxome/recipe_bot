import random
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'my_super_secret_CODE_eveR'
app.config['UPLOAD_FOLDER'] = 'static/files'


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     login = db.Column(db.String(128), nullable=False, unique=True)
#     password = db.Column(db.String(255), nullable=False)


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


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('dashboard.html')


@app.route('/add_recipe', methods=['GET', 'POST'])
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
        return "ok"
    return render_template('add_recipe.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005)
