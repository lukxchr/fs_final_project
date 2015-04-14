from flask.ext.wtf import Form 
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NewRestaurantForm(Form):
	name = StringField('What is the name of the new restaurant?', validators=[Required()])
	submit = SubmitField('Submit')