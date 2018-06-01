from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import make_response
from sqlalchemy.orm import sessionmaker
#for anti forgery state token
from flask import session as login_session
import random, string

# database imports
from sqlalchemy import create_engine, asc

from database_setup import Base, User, Category, CategoryItem

import httplib2
import json
import requests

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

#CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

# Connect to database
app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalognousers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all Categories and Latest added items

@app.route('/')
@app.route('/catalogs')
def mainCatalogMenu():
    session = DBSession()
    categories = session.query(Category).all()
    items = session.query(CategoryItem).all()
    items.sort(key = lambda item: int(item.id), reverse = True)
    return render_template('mainCatalogMenu.html', recentItems = items[:3], categories = categories)


@app.route('/catalog/<categoryname>/Items')
def showCategoryAndItems(categoryname):
    session = DBSession()
    selectedCategory = session.query(Category).filter_by(name = categoryname).one()
    items = session.query(CategoryItem).filter_by(category_id = selectedCategory.id).all()
    categories = session.query(Category).all()
    return render_template('showCategory.html', items = items, category = selectedCategory, numofitems = len(items), categories = categories)

@app.route('/catalog/<categoryname>/<item>')
def showItemDescription(categoryname, item):
    session = DBSession()
    selectedCategory = session.query(Category).filter_by(name = categoryname).one()
    # so it knows which category in case of duplicate titles between categories
    item1 = session.query(CategoryItem).filter_by(name = item, category_id = selectedCategory.id).first()
    return render_template('showItemDescription.html', item = item1)

@app.route('/catalog/item/new', methods = ['GET', 'POST'])
def newCategoryItem():
    session = DBSession()
    if request.method == 'POST':
        chosenCategory = session.query(Category).filter_by(name = request.form["category"]).one()
        newItem = CategoryItem(name = request.form["name"], description = request.form["description"], category = chosenCategory, category_id = int(chosenCategory.id))
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategoryAndItems', categoryname = newItem.category.name))
    else:
        return render_template('newCategoryItem.html')

@app.route('/catalog/<itemname>/edit', methods = ['GET', 'POST'])
def editCategoryItem(itemname):
    session = DBSession()
    editedItem = session.query(CategoryItem).filter_by(name = itemname).first()
    if request.method == 'POST':
        category = session.query(Category).filter_by(name = request.form['category']).one()
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category = category
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showCategoryAndItems', categoryname = editedItem.category.name))
    else:
        return render_template('editCategoryItem.html', item = editedItem)

@app.route('/catalog/<itemname>/delete', methods = ['GET', 'POST'])
def deleteCategoryItem(itemname):
    session = DBSession()
    itemToDelete = session.query(CategoryItem).filter_by(name = itemname).first()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('mainCatalogMenu'))
    else:
        return render_template('deleteCategoryItem.html', item = itemToDelete)

# Create a state token to prevent reuqest forgery
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    print state
    login_session['state'] = state
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0', port = 8000)
