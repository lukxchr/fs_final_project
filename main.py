from flask import Flask, request, render_template, \
 redirect, url_for, flash, session
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
#import forms
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
#manager = Manager(app)
bootstrap = Bootstrap(app)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
	#return 'chuj'
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	form = NewRestaurantForm()
	if form.validate_on_submit():
		name = form.name.data
		flash('added restaurant %s' % name)
		#form.name.data = ''
		#session['name'] = name
		return redirect(url_for('newRestaurant'))
	return render_template('newrestaurant.html', form=form)
	#return 'create new restaurant'
	
@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
	return render_template('editrestaurant.html', restaurant_id=restaurant_id)
	return "edit restaurant with id=%d" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
	return render_template('deleterestaurant.html', restaurant_id=restaurant_id)
	return "delete restaurant with id=%d" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	return render_template('menu.html', items=items)
	return "show menu for restaurant with id=%d" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):

	return render_template('newmenuitem.html', restaurant_id=restaurant_id)
	return "Add new menu item to restaurant id=%d" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/edit')
def editMenuItem(restaurant_id, item_id):
	return render_template('editmenuitem.html', restaurant_id=restaurant_id, item_id=item_id)
	return "edit menu item to restaurant id=%d menu_id=%d" % (restaurant_id, menu_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/delete/')
def deleteMenuItem(restaurant_id, item_id):
	return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item_id=item_id)
	return "delete menu item  restaurant id=%d menu_id =%d" % (restaurant_id, menu_id)

@app.errorhandler(404)
def pageNotFound(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internalServerError(e):
	return "internalServerError 500", 500

@app.route('/info/')
def info():
	#return str(app.config.keys)
	output = ""
	output += str([h for h in request.headers])
	output += "<br><br>"
	output += request.headers.get('User-Agent')
	return output, 400, {'chuj' : 'kasne-mleko'}

if __name__ == '__main__':
	app.run(debug=True)