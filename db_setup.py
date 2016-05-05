import json
import sys
from config import db, logger
from models import Beer, Brewery, Style
import unicodedata

def insert_beer(beer_list) :
	for beer in beer_list :
		# print(beer)
		# print("\n")d
		if beer.get("name") is not None :
			string_name = unicodedata.normalize('NFKD', beer.get("name")).encode('ascii','ignore')
		else :
			continue

		if beer.get("description") is not None :
			string_desc = unicodedata.normalize('NFKD', beer.get("description")).encode('ascii','ignore')
		else :
			continue

		if beer.get("labels") is not None :
			beer_image = beer.get("labels").get("large")
		else :
			continue

		if beer.get('isOrganic') is None or beer.get("abv") is None or beer.get("ibu") is None or beer.get("breweryId") is None or beer.get("styleId")  is None or beer_image  is None:
			continue

		b = Beer(name=string_name, description=string_desc, is_organic=beer.get('isOrganic'), abv=beer.get("abv"), ibu=beer.get("ibu"), scrape_brew_id=beer.get("breweryId"), scrape_style_id=beer.get("styleId"), image=beer_image)
		db.session.add(b)
		db.session.commit()

		if beer.get("name") is not None:
			logger.info("beer: " + beer.get("name") + " populated")

	db.session.commit()


def insert_brewery(brewery_list, loc_dict) :
	for brewery in brewery_list :

		# query for beers and make the relationship
		beer_inventory = db.session.query(Beer).filter(Beer.scrape_brew_id == brewery.get("id")).all()
		if len(beer_inventory) == 0:
			continue

		if brewery.get("name") is not None:
			string_name = unicodedata.normalize('NFKD', brewery.get("name")).encode('ascii', 'ignore')
		else :
			for row in beer_inventory:
				db.session.query(Beer).filter(Beer.beer_id == row.beer_id).delete()
			db.session.commit()
			continue

		if brewery.get("description") is not None :
			string_desc = unicodedata.normalize('NFKD', brewery.get("description")).encode('ascii','ignore')
		else :
			for row in beer_inventory:
				db.session.query(Beer).filter(Beer.beer_id == row.beer_id).delete()
			db.session.commit()
			continue

		if brewery.get("images") is not None :
			brew_icon = brewery.get("images").get("icon")
			brew_image = brewery.get("images").get("large")
		else :
			for row in beer_inventory:
				db.session.query(Beer).filter(Beer.beer_id == row.beer_id).delete()
			db.session.commit()
			continue

		loc_obj = loc_dict.get(brewery.get("id"))
		brew_loc = None
		if loc_obj is not None and loc_obj.get("locality") is not None and loc_obj.get("region") is not None:
			brew_loc = loc_obj.get("locality")
			brew_loc += ", "
			brew_loc +=  loc_obj.get("region")
		else :
			for row in beer_inventory:
				db.session.query(Beer).filter(Beer.beer_id == row.beer_id).delete()
			db.session.commit()
			continue

		if brew_loc is not None:
			brew_loc = unicodedata.normalize('NFKD', brew_loc).encode('ascii','ignore')
		else :
			for row in beer_inventory:
				db.session.query(Beer).filter(Beer.beer_id == row.beer_id).delete()
			db.session.commit()
			continue

		if brewery.get("website") is None or brewery.get("isOrganic") is None or brewery.get("established") is None:
			for row in beer_inventory:
				db.session.query(Beer).filter(Beer.beer_id == row.beer_id).delete()
			db.session.commit()
			continue

		# add the data and commit
		b = Brewery(name=string_name, description=string_desc, website=brewery.get("website"), is_organic=brewery.get("isOrganic"), icon=brew_icon, image=brew_image, established=brewery.get("established"), location=brew_loc)

		# for beer in db.session.query(Beer).filter(Beer.scrape_brew_id == brewery.get("id")) :
		# 	b.beers.append(beer)
		# for brew_beer_id in brewery.get("beerIds") :
		# 	b.beers.append(db.session.query(Beer).filter(Beer.beer_id == brew_beer_id))
		b.beers = beer_inventory

		db.session.add(b)
		db.session.commit()

		if brewery.get("name") is not None:
			logger.info("brewery: " + brewery.get("name") +  " populated with " + str(len(beer_inventory)) + " beers")

	# test = Brewery(name="Bob")
	# db.session.add(test)
	db.session.commit()

def insert_style(style_list) :
	for style in style_list :

		# query for beers and make the relationship
		beer_inventory = db.session.query(Beer).filter(Beer.scrape_style_id == style.get("id")).all()

		if style.get("name") is not None:
			string_name = unicodedata.normalize('NFKD', style.get("name")).encode('ascii', 'ignore')
		else :
			for item in beer_inventory :
				db.session.query(Beer).filter(Beer.beer_id == item.beer_id).delete()
			db.session.commit()
			continue

		if style.get("description") is not None :
			string_desc = unicodedata.normalize('NFKD', style.get("description")).encode('ascii','ignore')
		else :
			for item in beer_inventory :
				db.session.query(Beer).filter(Beer.beer_id == item.beer_id).delete()
			db.session.commit()
			continue

		if style.get("ibuMin") is None or style.get("ibuMax") is None or style.get("abvMin") is None or style.get("abvMax") is None :
			for item in beer_inventory :
				db.session.query(Beer).filter(Beer.beer_id == item.beer_id).delete()
			db.session.commit()
			continue

		# add the data and commit
		s = Style(name=string_name, description=string_desc, ibu_min=style.get("ibuMin"), ibu_max=style.get("ibuMax"), abv_min=style.get("abvMin"), abv_max=style.get("abvMax"))

		s.beers = beer_inventory

		db.session.add(s)
		db.session.commit()

		if style.get("name") is not None:
			logger.info("style: " + style.get("name") + " populated")

	db.session.commit()



def build_loc_dict(loc_list) :
	loc_dict = dict()
	for loc in loc_list :
		loc_dict[loc['breweryId']] = loc

	return loc_dict

def insert_data() :
	logger.info("Inserting data into db")
	with open("beers.json") as beer_json:
		beer_list = json.load(beer_json)

	insert_beer(beer_list)

	with open("breweries.json") as brew_json:
		brewery_list = json.load(brew_json)

	with open("locations.json") as loc_json :
		loc_list = json.load(loc_json)

	# optimizing lookup time when creating breweries
	loc_dict = build_loc_dict(loc_list)

	insert_brewery(brewery_list, loc_dict)

	with open("styles.json") as style_json:
		style_list = json.load(style_json)

	insert_style(style_list)
