from main import Restaurant, MenuItem, db
from random import random

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'0.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

#remove all records from all tables
def resetTables():
	db.drop_all()
	db.create_all()

def addRestaurants():
	db.session.add_all([Restaurant(id=r['id'], name=r['name']) for r in restaurants])
	db.session.commit()

def addMenuItems():
	db.session.add_all([MenuItem(id=i['id'], name=i['name'], description=i['description'], price=float(i['price']), course=i['course'], restaurant_id=int(random()*4+1)) for i in items])
	db.session.commit()

def resetAndCreateAll():
	resetTables()
	addRestaurants()
	addMenuItems()