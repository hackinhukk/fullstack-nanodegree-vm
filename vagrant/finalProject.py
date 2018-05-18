from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from database_setup import Base, Restaurant, MenuItem

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'}]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


app = Flask(__name__)

#engine = create_engine('sqlite:///restaurantmenu.db')
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
#session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new')
def newRestaurant():
    return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return render_template('editRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return render_template('deleteRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return render_template('menu.html', items = items, restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/new')
def newMenuItem(restaurant_id, menu_id):
    return render_template('newMenuItem.html')

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return render_template('editMenuItem.html', item = item)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return render_template('deleteMenuItem.html', item = item)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
