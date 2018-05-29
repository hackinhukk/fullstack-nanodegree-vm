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

# create category items for each one

cleatsCatItem = CategoryItem(name = 'Cleats', description = "They are useful for running on grass terrain in soccer",
                            category = soccerCategory, user = User1)

session.add(cleatsCatItem)
session.commit()

shootingSleeveCatItem = CategoryItem(name = "Shooting Sleeve", description = "To look cool while shooting a basketball",
                                    category = basketballCategory, user = User1)
session.add(shootingSleeveCatItem)
session.commit()

baseballCatItem = CategoryItem(name = "Baseball", description = "The seamed ball that is used in baseball.",
                              category = baseballCategory, user = User1)
session.add(baseballCatItem)
session.commit()

frisbeeDiscCatItem = CategoryItem(name = "Frisbee Disc", description = "The disc that players throw around during the game.",
                                 category = frisbeeCategory, user = User1)
session.add(frisbeeDiscCatItem)
session.commit()

snowboardCatItem = CategoryItem(name = "Snowboard", description = "The board that is used to get down a mountain.  Both legs are strapped into the singular board.",
                                category = snowboardingCategory, user = User1)
session.add(snowboardCatItem)
session.commit()

climbingGlovesCatItem = CategoryItem(name = "Rock Climbing Gloves", description = "Help provide grip and protection to your hands when rock climbing outdoors or indoors",
                                    category = rockClimbingCategory, user = User1)
session.add(climbingGlovesCatItem)
session.commit()

helmetCatItem = CategoryItem(name = "Football Helmet", description = "Used to protect head from concussions and other various head trauma injuries.",
                            category = foosballCategory, user = User1)
session.add(helmetCatItem)
session.commit()

rollerBladesCatItem = CategoryItem(name = "Roller Blades", description = "Used for indoor or outdoor skating on solid ground.",
                                  category = skatingCategory, user = User1)
session.add(rollerBladesCatItem)
session.commit()

goalieNetCatItem = CategoryItem(name = 'Goalie Net', description = "Where offensive players put the puck in to score a goal.",
                                category = hockeyCategory, user = User1)
session.add(goalieNetCatItem)
session.commit()

print "added catalog items!"
