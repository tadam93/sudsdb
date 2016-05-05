import logging
# from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
# from sqlalchemy.ext.declarative import declarative_base
from config import db

# engine = create_engine('sqlite:///:memory:', echo=True)

# Base = declarative_base()

class Beer(db.Model) :
	"""
	The Beer Table

	-Contains entries for every beer that has attributes:
		name : String(256)
		description : String(16384)
		is_organic : String(1)
		abv : Float
		beer_id : Integer
		ibu : Integer
		image : String(256)

	-Has a "brewery_id" foreign key to help establish the 1-to-many relationship between
	beer and brewery (many beers per brewery, but one brewery per beer)
	-Has a "style_id" foreign key to help esatblish the 1-to-many relationship between
	beer and style

	"""
	__tablename__ = 'beer'

	name = db.Column(db.String(256), nullable=False)
	description = db.Column(db.String(16384))
	is_organic = db.Column(db.String(1))
	abv = db.Column(db.Float(1))
	ibu = db.Column(db.Integer)
	beer_id = db.Column(db.Integer, primary_key=True)
	brewery_id = db.Column(db.Integer, db.ForeignKey('brewery.brewery_id'))
	style_id = db.Column(db.Integer, db.ForeignKey('style.style_id'))
	image = db.Column(db.String(256))

	# these attributes are needed for adding relationships later
	scrape_brew_id = db.Column(db.String(256))
	scrape_style_id = db.Column(db.Integer)


	def __repr__(self) :
		return "<Beer('%s', '%s', '%s')>" % (self.name, self.is_organic, self.abv)


class Brewery(db.Model) :
	"""
	The Brewery Table

	-Contains entries for every brewery that has attributes:
		name : String(256)
		description : String(16384)
		brewery_id : Integer
		website : String(256)
		icon : String(256)
		is_organic : String(1)
		image : String(256)
		established : String(10)
		location : String(80)

	-Has a beers attribute that stores all the beers that belong to this
	brewery. Helps set up the one to many relationship between beers and
	brewers as well.

	"""
	__tablename__ = 'brewery'

	name = db.Column(db.String(256))

	description = db.Column(db.String(16384))
	brewery_id = db.Column(db.Integer, primary_key=True)
	website = db.Column(db.String(256))
	icon = db.Column(db.String(256))
	is_organic = db.Column(db.String(1))
	image = db.Column(db.String(256))
	established = db.Column(db.String(10))
	location = db.Column(db.String(80))

	beers = db.relationship("Beer", backref="brewery")

	def __repr__(self) :
		return "<Brewery('%s', '%s')>" % (self.name, self.website)

class Style(db.Model) :
	"""
	The Style Table

	-Contains entries for every style that has attributes:
		style_id : Integer
		name : String(256)
		description : String(16384)
		ibu_min : Integer
		ibu_max : Integer
		abv_min : Integer
		abv_max : Integer

	-Has a beers attribute that stores all the beers that are of this
	style. Helps set up the one to many relationship between beers and
	styles as well.
	"""

	__tablename__ = "style"

	style_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(256), nullable=False)
	description = db.Column(db.String(16384))
	ibu_min = db.Column(db.Integer)
	ibu_max = db.Column(db.Integer)
	abv_min = db.Column(db.Integer)
	abv_max = db.Column(db.Integer)

	beers = db.relationship("Beer", backref="style")

	def __repr__(self) :
		return "<Style('%s')>" % (self.name)


# print(db.create_all())
