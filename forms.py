from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SelectField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired

class ProductForm(FlaskForm):
    image = FileField('Product Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    title = StringField('Title', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('electronics', 'Electronics'), ('clothing', 'Clothing'), ('books', 'Books')], validators=[DataRequired()])
