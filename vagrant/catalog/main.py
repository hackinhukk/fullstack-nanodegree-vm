from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import make_response
from flask import session as login_session
# database imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, CategoryItem

import string
import httplib2
import json
import requests


app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalognousers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all Categories and Latest added items

@app.route('/')
@app.route('/catalog')
def mainCatalogMenu():
    session = DBSession()
    categories = session.query(Category).all()
    items = session.query(CategoryItem).all()
    items.sort(key = lambda item: int(item.id), reverse = True)
    return render_template('mainCatalogMenu.html', recentItems = items[:3], categories = categories)


@app.route('/catalog/<categoryname>/Items')
def showCategory(categoryname):
    session = DBSession()
    selectedCategory = session.query(Category).filter_by(name = categoryname).one()
    items = session.query(CategoryItem).filter_by(category_id = selectedCategory.id)
    print selectedCategory.name
    print items
    return render_template('showCategory.html', items = items, category = selectedCategory)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0', port = 8000)
