from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, CategoryItem

engine = create_engine('sqlite:///itemcatalog.db')


Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

session = DBSession()

# create dummy user
User1 = User(name = "TNT", email = 'xdww@gmail.com')
session.add(User1)
session.commit()

# Create base categories

soccerCategory = Category(name = 'Soccer')
session.add(soccerCategory)
session.commit()

basketballCategory = Category(name = 'Basketball')
session.add(basketballCategory)
session.commit()

baseballCategory = Category(name = 'Baseball')
session.add(baseballCategory)
session.commit()

frisbeeCategory = Category(name = 'Frisbee')
session.add(frisbeeCategory)
session.commit()

snowboardingCategory = Category(name = 'Snowboarding')
session.add(snowboardingCategory)
session.commit()

rockClimbingCategory = Category(name = 'Rock Climbing')
session.add(rockClimbingCategory)
session.commit()

foosballCategory = Category(name = 'Foosball')
session.add(foosballCategory)
session.commit()

skatingCategory = Category(name = 'Skating')
session.add(skatingCategory)
session.commit()

hockeyCategory = Category(name = 'Hockey')
session.add(hockeyCategory)
session.commit()

#create menu items for each one
