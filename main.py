from flask import Flask, request, render_template, \
 redirect, url_for, flash, session, jsonify
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
#import forms
from forms import *
import os.path

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
bootstrap = Bootstrap(app)


#database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = Restaurant.query.all()
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	form = RestaurantForm()
	if form.validate_on_submit():
		name = form.name.data
		#add new restaurant with specified name to the db
		new_restaurant = Restaurant(name=name)
		db.session.add(new_restaurant)
		db.session.commit()
		flash('New Restaurant Created')
		return redirect(url_for('showRestaurants'))
	return render_template('newrestaurant.html', form=form)
	
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
	form = RestaurantForm(name = restaurant.name)
	if form.validate_on_submit():
		name = form.name.data
		restaurant.name = name
		db.session.add(restaurant)
		db.session.commit()
		flash('Restaurant Successfully Edited')
		return redirect(url_for('showRestaurants'))
	return render_template('editrestaurant.html', restaurant=restaurant, form=form)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
	if request.method == 'POST':
		#if user confirmed delete restaurant, otherwise skip to redirect
		action = request.form.get('delete_restaurant')
		#action == 'delete' iff user clicked delete button
		if action == 'delete':
			#delete MenuItems associated with Restaurant
			items = MenuItem.query.filter_by(restaurant_id=restaurant.id)
			n_items = items.count()
			for item in items.all():
				db.session.delete(item)
			flash_message = 'Successfully Deleted {0} Menu Items'.format(n_items) \
				if (n_items > 0) else 'No Menu Items were deleted'
			flash(flash_message)
			db.session.delete(restaurant)
			db.session.commit()
			flash('Restaurant Successfully Deleted')
		return redirect(url_for('showRestaurants'))
	return render_template('deleterestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
	items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
	return render_template('menu.html', items=items, restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	form = MenuItemForm()
	restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
	if form.validate_on_submit():
		name = form.name.data
		description = form.description.data
		price = form.price.data
		course = form.course.data
		new_menu_item = MenuItem(name=name, description=description, 
			price=price, course=course, restaurant_id=restaurant_id)
		print new_menu_item
		db.session.add(new_menu_item)
		db.session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	return render_template('newmenuitem.html', restaurant=restaurant, form=form)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
	restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
	item = MenuItem.query.filter_by(id=item_id).first()
	form = MenuItemForm(name=item.name, description=item.description, 
		price=item.price, course=item.course)
	if form.validate_on_submit():
		item.name = form.name.data
		item.description = form.description.data
		item.price = form.price.data
		item.course = form.course.data
		db.session.add(item)
		db.session.commit()
		flash('Menu Item Successfully Edited')
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	return render_template('editmenuitem.html', form=form, item=item)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, item_id):
	restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
	item = MenuItem.query.filter_by(id=item_id).first()
	if request.method == 'POST':
		#if user confirmed delete item, otherwise skip to redirect
		action = request.form.get('delete_item')
		if action == 'delete':
			db.session.delete(item)
			db.session.commit()
			flash('Menu Item Successfully Deleted')
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	return render_template('deletemenuitem.html', restaurant=restaurant, item=item)

@app.errorhandler(404)
def pageNotFound(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internalServerError(e):
	return "internalServerError 500", 500


#temporary view functions for debugging purposes
@app.route('/info/')
def info():
	#return str(app.config.keys)
	output = ""
	output += str([h for h in request.headers])
	output += "<br><br>"
	output += request.headers.get('User-Agent')
	return output, 400

#all restaurants
@app.route('/restaurants/JSON/')
def restaurantsJSON():
	restaurants = Restaurant.query.all()
	return jsonify(Restaurants=[r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
	items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/JSON')
def MenuItemJSON(restaurant_id, item_id):
	item = MenuItem.query.filter_by(restaurant_id=restaurant_id, id=item_id).first()
	return jsonify(item.serialize)

#db model definitions
class Restaurant(db.Model):
	__tablename__ = 'restaurants'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, index=True)
	manu_items = db.relationship('MenuItem', backref='restaurant') 

	def __repr__(self):
		return "<Restaurant %s>" % self.name

	@property
	def serialize(self):
	    return {
	    	'id' : self.id, 
	    	'name' : self.name
	    }
	

class MenuItem(db.Model):
	__tablename__ = 'menu_items'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	description = db.Column(db.String(200))
	price = db.Column(db.Numeric())
	course = db.Column(db.String(64))
	restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

	def __repr__(self):
		return "<MenuItem %s -- %s -- %d -- %s -- (%d)>" % (
			self.name, self.description, self.price, self.course, self.restaurant_id)

	@property
	def serialize(self):
		return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
           'price'         : '{0}'.format(round(self.price, 2)),
           'course'         : self.course,
       }

if __name__ == '__main__':
	#app.run(debug=True)
	manager.run()