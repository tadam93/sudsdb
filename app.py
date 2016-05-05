import math
import json, unicodedata
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.error import URLError

from io import StringIO
from flask import render_template, jsonify, Markup
from config import app, db, manager, logger
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_

from models import Beer, Brewery, Style
from db_setup import insert_data

from static_routes import StaticRouter
from search_routes import SearchRouter
from details_routes import DetailRouter

import subprocess
import api
import re
import sys


@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

app.add_url_rule('/', StaticRouter.index)
app.add_url_rule('/about', StaticRouter.about)
app.add_url_rule('/breweries', StaticRouter.breweries)
app.add_url_rule('/beers', StaticRouter.beers)
app.add_url_rule('/styles', StaticRouter.styles)

app.add_url_rule('/search/<string:terms>', SearchRoutes.search)

app.add_url_rule('/beers/<int:beer>', DetailRouter.beer)
app.add_url_rule('/breweries/<int:brewery>', DetailRouter.brewery)
app.add_url_rule('/styles/<int:style>', DetailRouter.style)


@app.route('/api/beers', methods=["GET"])
def beers():
    return jsonify({'beers': list(map(api.get_beer_details, Beer.query.all()))})

@app.route('/api/beers/<int:page_num>/sort/<sort_col>/<sort_direction>', methods=["GET"])
def beers_sorted(page_num, sort_col, sort_direction):
    if sort_direction == 'asc':
        query = db.session.query(Beer).outerjoin(Brewery, Beer.brewery_id == Brewery.brewery_id).outerjoin(Style, Beer.scrape_style_id == Style.style_id).order_by(sort_col + " asc").limit(20).offset(page_num * 20).all();
        data = {'beers_sorted': list(map(api.get_beer_details, query))};
        return jsonify(data)
    elif sort_direction == 'desc':
        query = db.session.query(Beer).outerjoin(Brewery, Beer.brewery_id == Brewery.brewery_id).outerjoin(Style, Beer.scrape_style_id == Style.style_id).order_by(sort_col + " desc").limit(20).offset(page_num * 20).all();
        data = {'beers_sorted': list(map(api.get_beer_details, query))};
        return jsonify(data)

@app.route('/api/beers/get_num', methods=["GET"])
def beers_get_num():
    page_num = math.ceil(Beer.query.count() / 20)
    return jsonify({'beers_get_num': page_num})


@app.route('/api/beers/<int:beer_id>', methods=["GET"])
def beer(beer_id):
    return jsonify({'beer': api.get_beer_details(Beer.query.filter_by(beer_id=beer_id).first())})

@app.route('/api/breweries', methods=["GET"])
def breweries():
    return jsonify({'breweries': list(map(api.get_brewery_details, Brewery.query.all()))})

@app.route('/api/breweries/<int:page_num>/sort/<sort_col>/<sort_direction>', methods=["GET"])
def breweries_sorted(page_num, sort_col, sort_direction):
    if sort_direction == 'asc':
        query = db.session.query(Brewery).order_by(sort_col + " asc").limit(20).offset(page_num * 20).all();
        data = {'breweries_sorted': list(map(api.get_brewery_details, query))};
        return jsonify(data)
    elif sort_direction == 'desc':
        query = db.session.query(Brewery).order_by(sort_col + " desc").limit(20).offset(page_num * 20).all();
        data = {'breweries_sorted': list(map(api.get_brewery_details, query))};
        return jsonify(data)

@app.route('/api/breweries/get_num', methods=["GET"])
def breweries_get_num():
    page_num = math.ceil(Brewery.query.count()/ 20)
    return jsonify({'breweries_get_num': page_num})

@app.route('/api/breweries/<int:brewery_id>', methods=["GET"])
def brewery(brewery_id):
    return jsonify({'brewery': api.get_brewery_details(Brewery.query.filter_by(brewery_id=brewery_id).first())})

@app.route('/api/styles', methods=["GET"])
def styles():
    return jsonify({'styles': list(map(api.get_style_details, Style.query.all()))})

@app.route('/api/styles/<int:page_num>/sort/<sort_col>/<sort_direction>', methods=["GET"])
def styles_sorted(page_num, sort_col, sort_direction):
    if sort_direction == 'asc':
        query = db.session.query(Style).order_by(sort_col + " asc").limit(20).offset(page_num * 20).all();
        data = {'styles_sorted': list(map(api.get_style_details, query))};
        return jsonify(data)
    elif sort_direction == 'desc':
        query = db.session.query(Style).order_by(sort_col + " desc").limit(20).offset(page_num * 20).all();
        data = {'styles_sorted': list(map(api.get_style_details, query))};
        return jsonify(data)

@app.route('/api/styles/get_num', methods=["GET"])
def styles_get_num():
    page_num = math.ceil(Style.query.count() / 20)
    return jsonify({'styles_get_num': page_num})

@app.route('/api/styles/<int:style_id>', methods=["GET"])
def style(style_id):
    return jsonify({'style': api.get_style_details(Style.query.filter_by(style_id=style_id).first())})


@app.route('/api/search/<string:category>/<string:terms>/<int:page>')
def search(category, terms, page):
    #terms = terms.replace("%20", " ")
    data = []
    original_case_terms = terms;
    lterms = terms.split(" ")
    iterms = iter(lterms)
    init_or = next(iterms)
    if category == 'beers':# if beers
        and_query = db.session.query(Beer).filter(or_(Beer.name.like("%" + terms + "%"), Beer.description.like("%" + terms + "%"), Beer.abv.like("%" + terms + "%"), Beer.ibu.like("%" + terms + "%")))
        no_context_data = and_query.order_by("name asc").limit(20).offset(page * 20).all()
        no_context_data =  list(map(api.get_beer_details, no_context_data))
        and_count = and_query.count()
        for res in no_context_data:
            res["rclass"] = "and-res"
        #check query for searches that match an individual word.
        or_query = db.session.query(Beer).filter(or_(Beer.name.like("%" + init_or + "%"), Beer.description.like("%" + init_or + "%"), Beer.abv.like("%" + init_or + "%"), Beer.ibu.like("%" + init_or + "%")))
        for term in iterms:
            or_query = or_query.union(db.session.query(Beer).filter(or_(Beer.name.like("%" + term + "%"), Beer.description.like("%" + term + "%"), Beer.abv.like("%" + term + "%"), Beer.ibu.like("%" + term + "%"))))
        #filter out duplicates from and_query. NOTE: make cleaner if time exists
        or_query = or_query.filter(Beer.beer_id.notin_(db.session.query(Beer.beer_id).filter(or_(Beer.name.like("%" + terms + "%"), Beer.description.like("%" + terms + "%"), Beer.abv.like("%" + terms + "%"), Beer.ibu.like("%" + terms + "%")))))
        #populate page with additional results from or.
        if(len(no_context_data) < 20) :
            no_context_or = or_query.limit(20 - len(no_context_data)).offset((page-and_count/20)*20+and_count%20).all()
            no_context_or =  list(map(api.get_beer_details, no_context_or))
            for res in no_context_or:
                res["rclass"] = "or-res"
            no_context_data += no_context_or
    elif category == 'breweries':# if breweries
        and_query = db.session.query(Brewery).filter(or_(Brewery.name.like("%" + terms + "%"), Brewery.description.like("%" + terms + "%"), Brewery.website.like("%" + terms + "%"), Brewery.established.like("%" + terms + "%"),  Brewery.location.like("%" + terms + "%")))
        no_context_data = and_query.order_by("name asc").limit(20).offset(page * 20).all()
        no_context_data =  list(map(api.get_brewery_details, no_context_data))
        and_count = and_query.count()
        for res in no_context_data:
            res["rclass"] = "and-res"
        #filter out duplicates from and_query. NOTE: make cleaner if time exists
        or_query = db.session.query(Brewery).filter(or_(Brewery.name.like("%" + init_or + "%"), Brewery.description.like("%" + init_or + "%"), Brewery.website.like("%" + init_or + "%"), Brewery.established.like("%" + init_or + "%"),  Brewery.location.like("%" + init_or + "%")))
        for term in iterms:
            or_query = or_query.union(db.session.query(Brewery).filter(or_(Brewery.name.like("%" + term + "%"), Brewery.description.like("%" + term + "%"), Brewery.website.like("%" + term + "%"), Brewery.established.like("%" + term + "%"),  Brewery.location.like("%" + term + "%"))))
        or_query = or_query.filter(Brewery.brewery_id.notin_(db.session.query(Brewery.brewery_id).filter(or_(Brewery.name.like("%" + terms + "%"), Brewery.description.like("%" + terms + "%"), Brewery.website.like("%" + terms + "%"), Brewery.established.like("%" + terms + "%"),  Brewery.location.like("%" + terms + "%")))))
        #populate page with additional results from or.
        if(len(no_context_data) < 20) :
            no_context_or = or_query.limit(20 - len(no_context_data)).offset((page-and_count/20)*20+and_count%20).all()
            no_context_or =  list(map(api.get_brewery_details, no_context_or))
            for res in no_context_or:
                res["rclass"] = "or-res"
            no_context_data += no_context_or
    elif category == 'styles': # if styles
        and_query = db.session.query(Style).filter(or_(Style.name.like("%" + terms + "%"), Style.description.like("%" + terms + "%"), Style.ibu_min.like("%" + terms + "%"), Style.ibu_max.like("%" + terms + "%"), Style.abv_min.like("%" + terms + "%"), Style.abv_max.like("%" + terms + "%")))
        no_context_data = and_query.order_by("name asc").limit(20).offset(page * 20).all()
        no_context_data =  list(map(api.get_style_details, no_context_data))
        and_count = and_query.count()
        for res in no_context_data:
            res["rclass"] = "and-res"
        #filter out duplicates from and_query. NOTE: make cleaner if time exists
        or_query = db.session.query(Style).filter(or_(Style.name.like("%" + init_or + "%"), Style.description.like("%" + init_or + "%"), Style.ibu_min.like("%" + init_or + "%"), Style.ibu_max.like("%" + init_or + "%"), Style.abv_min.like("%" + init_or + "%"), Style.abv_max.like("%" + init_or + "%")))
        for term in iterms:
            or_query = or_query.union(db.session.query(Style).filter(or_(Style.name.like("%" + term + "%"), Style.description.like("%" + term + "%"), Style.ibu_min.like("%" + term + "%"), Style.ibu_max.like("%" + term + "%"), Style.abv_min.like("%" + term + "%"), Style.abv_max.like("%" + term + "%"))))
        or_query = or_query.filter(Style.style_id.notin_(db.session.query(Style.style_id).filter(or_(Style.name.like("%" + terms + "%"), Style.description.like("%" + terms + "%"), Style.ibu_min.like("%" + terms + "%"), Style.ibu_max.like("%" + terms + "%"), Style.abv_min.like("%" + terms + "%"), Style.abv_max.like("%" + terms + "%")))))
        #populate page with additional results from or.
        if(len(no_context_data) < 20) :
            no_context_or = or_query.limit(20 - len(no_context_data)).offset((page-and_count/20)*20+and_count%20).all()
            no_context_or =  list(map(api.get_style_details, no_context_or))
            for res in no_context_or:
                res["rclass"] = "or-res"
            no_context_data += no_context_or
    or_count = or_query.count()
    page_num = math.ceil((and_count+or_count)/ 20)

    #bolding currently doesn't check for individual words in a search
    data = []
    lterm = iter(lterms)
    rterm = "(" + next(lterm)
    for term in lterms:
        rterm += "|" + term
    rterm += ")"
    for row in no_context_data:
        formatted_row = {}
        for key in row:
            mterm = terms
            if type(row[key]) == int or type(row[key]) == float or key == 'image' or key == 'icon' or key == 'website' or type(row[key]) == list:
                formatted_row[key] = row[key]
                continue
            term_pos = row[key].casefold().find(mterm.casefold())
            if term_pos < 0:
                sres = re.search(rterm,row[key], re.IGNORECASE)
                if sres:
                    mterm = sres.group(0)
                    term_pos = term_pos = row[key].casefold().find(mterm.casefold())
            if len(row[key]) > 30 and term_pos > -1:
                row[key] = "..." + row[key][term_pos:term_pos + 25] + "..."
            elif len(row[key]) > 30:
                row[key] = row[key][:28] + "..."
            term_pos = row[key].casefold().find(mterm.casefold()) #index of term may have changed because of ...
            if term_pos > -1: # this section adds the "bolding" to the text. must come after ...
                pre_str = row[key][0:term_pos]
                post_str = row[key][term_pos + len(mterm):]
                row[key] = pre_str + "<strong>" + row[key][term_pos:term_pos + len(mterm)] + "</strong>" + post_str
            formatted_row[key] = row[key]
        data.append(formatted_row);
    return jsonify({'results': data, "terms" : terms, 'max_page': page_num})

def create_db():
    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
	commands = {
        "create_db": create_db,
		"insert_data": insert_data
	}
	if len(sys.argv) > 1 :
		try:
			commands[sys.argv[1]]()
		except Exception as instance:
			logger.error("Invalid command")
			logger.error(instance.args)
	else:
		logger.info("\tpython3 db_setup.py command\n\n" +
                    "\tcreate_db\t drops and then recreates the database" +
                    "\tinsert_data\t inserts all data into db (may take several minutes)")
