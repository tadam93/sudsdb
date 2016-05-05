import json
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
import unicodedata

Base = declarative_base()

class Beer(Base) :
	"""
	The Beer Table
	-Contains entries for every beer that has attributes:
		name : String(256)
		description : String(256)
		is_organic : String(1)
		abv : Float
		beer_id : Integer
		ibu : Integer
	-Has a "brewery_id" foreign key to help establish the 1-to-many relationship between
	beer and brewery (many beers per brewery, but one brewery per beer)
	-Has a "style_id" foreign key to help esatblish the 1-to-many relationship between
	beer and style
	"""
	__tablename__ = 'beer'

	name = Column(String(256), nullable=False)
	description = Column(String(256))
	is_organic = Column(String(1))
	abv = Column(Float(1))
	ibu = Column(Integer)
	beer_id = Column(Integer, primary_key=True)
	brewery_id = Column(Integer, ForeignKey('brewery.brewery_id'))
	style_id = Column(Integer, ForeignKey('style.style_id'))

	scrape_brew_id = Column(String(256))
	scrape_style_id = Column(Integer)


	def __repr__(self) :
		return "<Beer('%s', '%s', '%s')>" % (self.name, self.is_organic, self.abv)


class Brewery(Base) :
	"""
	The Brewery Table
	
	-Contains entries for every brewery that has attributes:
		name : String(256)
		description : String(256)
		brewery_id : Integer
		website : String(256)
		icon : Image
		is_organic : String(1)
	-Has a beers attribute that stores all the beers that belong to this 
	brewery. Helps set up the one to many relationship between beers and
	brewers as well.
	"""
	__tablename__ = 'brewery'

	name = Column(String(256), nullable=False)

	description = Column(String(256))
	brewery_id = Column(Integer, primary_key=True)
	website = Column(String(256))
	icon = Column(String(256))
	is_organic = Column(String(1))
	location = Column(String(256))

	beers = relationship("Beer", backref="brewery")

	def __repr__(self) :
		return "<Brewery('%s', '%s')>" % (self.name, self.website)

class Style(Base) :
	"""
	The Style Table
	-Contains entries for every style that has attributes:
		style_id : Integer
		name : String(256)
		description : String(256)
		ibu_min : Integer
		ibu_max : Integer
		abv_min : Integer
		abv_max : Integer
	-Has a beers attribute that stores all the beers that are of this 
	style. Helps set up the one to many relationship between beers and
	styles as well.
	"""

	__tablename__ = "style"

	style_id = Column(Integer, primary_key=True)
	name = Column(String(256), nullable=False)
	description = Column(String(256))
	ibu_min = Column(Integer)
	ibu_max = Column(Integer)
	abv_min = Column(Integer)
	abv_max = Column(Integer)

	beers = relationship("Beer", backref="style")

	def __repr__(self) :
		return "<Style('%s')>" % (self.name)

engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)

session = Session()

def insert_beer(beer_list) :
	for beer in beer_list :
		# print(beer)
		# print("\n")
		if beer.get("name") is not None :
			string_name = unicodedata.normalize('NFKD', beer.get("name")).encode('ascii','ignore')
		else :
			string_name = None

		if beer.get("description") is not None :
			string_desc = unicodedata.normalize('NFKD', beer.get("description")).encode('ascii','ignore')
		else :
			string_desc = None

		b = Beer(name=string_name, description=string_desc, is_organic=beer.get('isOrganic'), abv=beer.get("abv"), ibu=beer.get("ibu"), scrape_brew_id=beer.get("breweryId"), scrape_style_id=beer.get("styleId"))
		session.add(b)
		session.commit()

	session.commit()

def insert_brewery(brewery_list, loc_dict) :

	for brewery in brewery_list :

		# query for beers and make the relationship
		beer_inventory = session.query(Beer).filter(Beer.scrape_brew_id == brewery.get("id")).all()

		# print(beer_inventory)

		if brewery.get("name") is not None:
			string_name = unicodedata.normalize('NFKD', brewery.get("name")).encode('ascii', 'ignore')
		else :
			string_name = None

		if brewery.get("description") is not None :
			string_desc = unicodedata.normalize('NFKD', brewery.get("description")).encode('ascii','ignore')
		else :
			string_desc = None

		if brewery.get("images") is not None :
			brew_icon = brewery.get("images").get("icon")
		else :
			brew_icon = None

		loc_obj = loc_dict.get(brewery.get("id"))
		brew_loc = None
		if loc_obj is not None and loc_obj.get("locality") is not None and loc_obj.get("region") is not None:
			brew_loc = loc_obj.get("locality")
			brew_loc += ", "
			brew_loc +=  loc_obj.get("region")

		if brew_loc is not None:
			brew_loc = unicodedata.normalize('NFKD', brew_loc).encode('ascii','ignore')
		print(brew_loc)

		# add the data and commit
		b = Brewery(name=string_name, description=string_desc, website=brewery.get("website"), is_organic=brewery.get("isOrganic"), icon=brew_icon, location=brew_loc)

		# for beer in db.session.query(Beer).filter(Beer.scrape_brew_id == brewery.get("id")) :
		# 	b.beers.append(beer)
		b.beers = beer_inventory
		# print(b.beers)
		session.add(b)
		session.commit()
	session.commit()

def build_loc_dict(loc_list) :
	loc_dict = dict()
	for loc in loc_list :
		loc_dict[loc['breweryId']] = loc

	return loc_dict



with open("beers.json") as beer_json:
	beer_list = json.load(beer_json)

# insert_beer(beer_list)

with open("breweries.json") as brew_json:
	brewery_list = json.load(brew_json)

with open("locations.json") as loc_json :
	loc_list = json.load(loc_json)

loc_dict = build_loc_dict(loc_list)

insert_brewery(brewery_list, loc_dict)



# print(session.query(Brewery).filter(Brewery.location == "Jackson, Michigan").first())