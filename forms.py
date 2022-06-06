from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired


class Product:
    def __init__(self, name, quantity, unit, unit_price):
       self.name = name
       self.quantity = quantity
       self.unit = unit
       self.unit_price = unit_price
  

    def get_items (self):
            return (f"{self.name}, {self.quantity}, {self.unit}, {self.unit_price}")


class ProductForm(FlaskForm):
   name = StringField('Name', validators=[DataRequired()])
   quantity = DecimalField('Quantity', validators=[DataRequired()])
   unit = StringField('Unit', validators=[DataRequired()])
   unit_price = DecimalField ('Price', validators=[DataRequired()])


