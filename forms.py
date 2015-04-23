from flask.ext.wtf import Form 
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import Required

# class NewRestaurantForm(Form):
# 	name = StringField('What is the name of the new restaurant?', validators=[Required()])
# 	submit = SubmitField('Submit')

# class EditRestaurantForm(Form):
# 	name = StringField('New name:', validators=[Required()])
# 	submit = SubmitField('Submit')


class RestaurantForm(Form):
	name = StringField('Name:', validators=[Required()])
	submit = SubmitField('Submit')

class MenuItemForm(Form):
	name = StringField('Name', validators=[Required()])
	description = StringField('Description', validators=[Required()])
	price = DecimalField('Price', validators=[Required()])
	course = SelectField('Course', choices=[('entree', 'Entree'), 
		('dessert', 'Dessert'), ('beverage', 'Beverage'), 
		('appetizer', 'Appetizer'), ('main_course', 'Main course')])
	submit = SubmitField('Submit')
