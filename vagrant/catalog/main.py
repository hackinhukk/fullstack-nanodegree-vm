from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy.orm import sessionmaker
# for anti forgery state token
from flask import session as login_session
import random
import string

# database imports
from sqlalchemy import create_engine, asc
from database_setup import Base, User, Category, CategoryItem


# for handling callback function from google oauth API

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

# Connect to database
app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
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
    items.sort(key=lambda item: int(item.id), reverse=True)
    if 'username' not in login_session:
        return render_template('publicMainCatalogMenu.html',
                               recentItems=items[:10], categories=categories)
    else:
        return render_template('mainCatalogMenu.html',
                               recentItems=items[:10], categories=categories)


@app.route('/catalog/<categoryname>/Items')
def showCategoryAndItems(categoryname):
    session = DBSession()
    selectedCategory = session.query(Category).filter_by(
                       name=categoryname).one()
    items = session.query(CategoryItem).filter_by(
            category_id=selectedCategory.id).all()
    categories = session.query(Category).all()
    if 'username' not in login_session:
        return render_template('publicShowCategory.html',
                               items=items, category=selectedCategory,
                               numofitems=len(items), categories=categories)
    else:
        return render_template('showCategory.html',
                               items=items, category=selectedCategory,
                               numofitems=len(items), categories=categories)


@app.route('/catalog/<categoryname>/<item>')
def showItemDescription(categoryname, item):
    session = DBSession()
    selectedCategory = session.query(Category).filter_by(
                       name=categoryname).one()
    # so it knows which category in case of duplicate titles between categories
    item1 = session.query(CategoryItem).filter_by(
            name=item, category_id=selectedCategory.id).first()
    creator = getUserInfo(item1.user_id)
    if ('username' not in login_session
            or creator.id != login_session['user_id']):
        return render_template('publicShowItemDescription.html', item=item1)
    else:
        return render_template('showItemDescription.html', item=item1)


@app.route('/catalog/item/new', methods=['GET', 'POST'])
def newCategoryItem():
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        catarr = ['Soccer', 'Basketball', 'Baseball', 'Frisbee',
                  'Snowboarding', 'Rock Climbing', 'Foosball',
                  'Skating', 'Hockey']
        if request.form['category'] in catarr:
            chosenCategory = session.query(Category).filter_by(
                             name=request.form["category"]).one()
            newItem = CategoryItem(name=request.form["name"],
                                   description=request.form["description"],
                                   category=chosenCategory,
                                   category_id=int(chosenCategory.id),
                                   user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            return redirect(url_for('showCategoryAndItems',
                                    categoryname=newItem.category.name))
        else:
            return render_template('newCategoryItem.html')
    else:
        return render_template('newCategoryItem.html')


@app.route('/catalog/<itemname>/edit', methods=['GET', 'POST'])
def editCategoryItem(itemname):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(CategoryItem).filter_by(name=itemname).first()
    creator = getUserInfo(editedItem.user_id)
    if creator.id != login_session['user_id']:
        return "<script type = 'text/javascript'>function myFunction() {alert('You are not authorized to edit this CategoryItem.  Please create your own CategoryItem in order to edit it.');}</script><body onload='myFunction();'>"
    if request.method == 'POST':
        category = session.query(Category).filter_by(
                   name=request.form['category']).one()
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category = category
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showCategoryAndItems',
                                categoryname=editedItem.category.name))
    else:
        return render_template('editCategoryItem.html', item=editedItem)


@app.route('/catalog/<itemname>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(itemname):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(CategoryItem).filter_by(name=itemname).first()
    if itemToDelete.user_id != login_session['user_id']:
        return "<script type = 'text/javascript'>function myFunction() {alert('You are not authorized to delete this CategoryItem.  Please create your own CategoryItem in order to delete it.');}</script><body onload='myFunction();'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('mainCatalogMenu'))
    else:
        return render_template('deleteCategoryItem.html', item=itemToDelete)


# Create a state token to prevent reuqest forgery
# Store it in the session for later validation


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    print state
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.header['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
                                 'Failed to upgrade the authorization code.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 50)
        response.headers['Content-Type'] = 'application/json'
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
                                 "Token's user ID doesn't match given"
                                 "user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
                                 "Token's client ID does not match app's"),
                                 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 'Current user is already connected'), 200)
        response.headers['Content-Type'] = 'application/sjon'

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get User Info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1> Welcome, '
    output += login_session['username']
    output += '!</h1>'
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session.


@app.route("/gdisconnect")
def gdisconnect():
    # Only disconnect a connected user
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps(
                                 'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Executte HTTP GET request to revoke current token.
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps(
                                 'Failed to revoke token for'
                                 'given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


# JSON Endpoint functions


@app.route('/catalogs/JSON')
def catalogsJSON():
    session = DBSession()
    catalogs = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in catalogs])


@app.route('/catalog/<itemname>/JSON')
def categoryItemJSON(itemname):
    session = DBSession()
    # in case of same named item, will show up the multi names
    item = session.query(CategoryItem).filter_by(name=itemname).all()
    return jsonify(item=[i.serialize for i in item])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0', port=8000)
