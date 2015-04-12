from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
	return 'This page will show all my restaurants'

@app.route('/restaurant/new/')
def newRestaurant():
	return 'create new restaurant'
	
@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
	return "edit restaurant with id=%d" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
	return "delete restaurant with id=%d" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	return "show menu for restaurant with id=%d" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
	return "Add new menu item to restaurant id=%d" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
	return "edit menu item to restaurant id=%d menu_id=%d" % (restaurant_id, menu_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	return "delete menu item  restaurant id=%d menu_id =%d" % (restaurant_id, menu_id)

if __name__ == '__main__':
	app.run(debug=True)