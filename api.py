def get_beer_details(beer):
	"""
	Returns a dictionary
	containing details of a beer
	"""

	beer_dict = dict()

	beer_dict['name'] = beer.name
	beer_dict['description'] = beer.description
	beer_dict['is_organic'] = beer.is_organic
	beer_dict['abv'] = beer.abv
	beer_dict['ibu'] = beer.ibu
	beer_dict['beer_id'] = beer.beer_id
	beer_dict['brewery_id'] = beer.brewery_id
	if beer.brewery is not None:
		beer_dict['brewery_name'] = beer.brewery.name
	beer_dict['style_id'] = beer.style_id
	if beer.style is not None:
		beer_dict['style_name'] = beer.style.name
	beer_dict['image'] = beer.image

	return beer_dict

def get_brewery_details(brewery):
	"""
	Returns a dictionary
	containing details of a brewery
	"""

	brewery_dict = dict()

	brewery_dict['name'] = brewery.name
	brewery_dict['description'] = brewery.description
	brewery_dict['brewery_id'] = brewery.brewery_id
	brewery_dict['website'] = brewery.website
	brewery_dict['icon'] = brewery.icon
	brewery_dict['is_organic'] = brewery.is_organic
	brewery_dict['image'] = brewery.image
	brewery_dict['established'] = brewery.established
	brewery_dict['location'] = brewery.location
	brewery_dict['beers'] = list(map(get_beer_details, brewery.beers))

	return brewery_dict

def get_style_details(style):
	"""
	Returns a dictionary
	containing details of a style
	"""

	style_dict = dict()

	style_dict['style_id'] = style.style_id
	style_dict['name'] = style.name
	style_dict['description'] = style.description
	style_dict['ibu_min'] = style.ibu_min
	style_dict['ibu_max'] = style.ibu_max
	style_dict['abv_min'] = style.abv_min
	style_dict['abv_max'] = style.abv_max
	style_dict['beers'] = list(map(get_beer_details, style.beers))

	return style_dict
