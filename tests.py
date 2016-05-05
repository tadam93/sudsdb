from unittest import main, TestCase
from models import Beer, Brewery, Style
from config import db, app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class TestSuds(TestCase):
    def test_creating_1(self):
        beer1 = Beer(name='Coors Light', description="Taste's like urine.",
            is_organic="N", abv=11.1, ibu=30)
        self.assertEqual(beer1.name, "Coors Light")
        self.assertEqual(beer1.is_organic, "N")
        self.assertEqual(beer1.beer_id, None)

    def test_creating_2(self) :
        b = Brewery(name="Austin's Brew House")

        self.assertEqual(b.name, "Austin's Brew House")
        self.assertEqual(b.website, None)

    def test_creating_3(self) :
        s = Style(name="Old Western Ale", description="Taste's like the old west")
        self.assertEqual(s.name, "Old Western Ale")
        self.assertEqual(s.description, "Taste's like the old west")
        self.assertEqual(s.style_id, None)

    def test_add_1(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

        beer1 = Beer(name='Coors Light', description="Taste's like urine.",
            is_organic="N", abv=12.2, ibu=30)
        beer2 = Beer(name='Blue Moon Original', description="A gift from heaven",
            is_organic="N", abv=9.8, ibu=70)

        db.session.add(beer1)
        db.session.add(beer2)
        db.session.commit()

        result = db.session.query(Beer).filter_by(abv=9.8).first()
        self.assertEqual(result.name, "Blue Moon Original")

        result = db.session.query(Beer).filter_by(name="Coors Light").first()
        self.assertEqual(result.ibu, 30)

        self.assertEqual(beer1.beer_id, 1)
        self.assertEqual(beer2.beer_id, 2)

    def test_add_2(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

        brewery1 = Brewery(name="Austin's Brew House")
        brewery2 = Brewery(name='The Brewski on 6th', description="Making good stuff",
            website="http://www.brew6th.com/")

        db.session.add(brewery1)
        db.session.add(brewery2)
        db.session.commit()

        result = db.session.query(Brewery).filter_by(name="Austin's Brew House").first()
        self.assertEqual(result.name, "Austin's Brew House")

        result = db.session.query(Brewery).filter_by(brewery_id=2).first()
        self.assertEqual(result.name, "The Brewski on 6th")

        self.assertEqual(brewery1.brewery_id, 1)
        self.assertEqual(brewery2.brewery_id, 2)

    def test_add_3(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

        style1 = Style(name="Old Western Ales")
        style2 = Style(name='Russian Blends', description="It's pretty much just vodka")

        db.session.add(style1)
        db.session.add(style2)
        db.session.commit()

        result = db.session.query(Style).filter_by(name="Old Western Ales").first()
        self.assertEqual(result.name, "Old Western Ales")

        result = db.session.query(Style).filter_by(style_id=2).first()
        self.assertEqual(result.description, "It's pretty much just vodka")

        self.assertEqual(style1.style_id, 1)
        self.assertEqual(style2.style_id, 2)

    def test_update_1(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

        beer1 = Beer(name='Coors Light', description="Taste's like urine.",
            is_organic="N", abv=11.1, ibu=30)

        db.session.add(beer1)
        db.session.commit()
        beer1.abv = 1234
        db.session.commit()

        result = db.session.query(Beer).filter_by(name="Coors Light").first()
        self.assertEqual(result.abv, 1234)

    def test_update_2(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

        b = Brewery(name="Austin's Brew House")

        db.session.add(b)
        db.session.commit()
        b.website = "http://www.austinbrew.com/"
        db.session.commit()

        result = db.session.query(Brewery).filter_by(name="Austin's Brew House").first()
        self.assertEqual(result.website, "http://www.austinbrew.com/")

    def test_update_3(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

        s = Style(name="Old Western Ale", description="Taste's like the old west")

        db.session.add(s)
        db.session.commit()
        s.name = "Old Eastern Ale"
        db.session.commit()

        result = db.session.query(Style).filter_by(name="Old Eastern Ale").first()
        self.assertEqual(result.description, "Taste's like the old west")

    def test_delete_1(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

        beer1 = Beer(name='Coors Light', description="Taste's like urine.",
            is_organic="N", abv=11.1, ibu=30)

        db.session.add(beer1)
        db.session.commit()
        self.assertEqual(beer1._sa_instance_state.persistent, True)

        db.session.delete(beer1)
        db.session.commit()
        self.assertEqual(beer1._sa_instance_state.persistent, False)

    def test_delete_2(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

        brewery1 = Brewery(name="Austin's Brew House")
        brewery2 = Brewery(name='The Brewski on 6th', description="Making good stuff",
            website="http://www.brew6th.com/")

        db.session.add(brewery1)
        db.session.add(brewery2)
        db.session.commit()

        self.assertEqual(brewery1._sa_instance_state.persistent, True)
        self.assertEqual(brewery2._sa_instance_state.persistent, True)

        db.session.delete(brewery1)
        db.session.commit()

        self.assertEqual(brewery1._sa_instance_state.persistent, False)
        self.assertEqual(brewery2._sa_instance_state.persistent, True)

    def test_delete_3(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

        style1 = Style(name="Old Western Ales")
        style2 = Style(name='Russian Blends', description="It's pretty much just vodka")

        db.session.add(style1)
        db.session.add(style2)
        db.session.commit()

        db.session.delete(style1)
        db.session.commit()

        self.assertEqual(style1._sa_instance_state.persistent, False)
        self.assertEqual(style2._sa_instance_state.persistent, True)

    def test_relationship_1(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

        coors_light = Beer(name='Coors Light', description="Taste's like urine.",
            is_organic="N", abv=11.1, ibu=30)
        austin_brew = Brewery(name="Austin's Brew House")
        db.session.add(coors_light)
        db.session.add(austin_brew)

        self.assertEqual(austin_brew.beers, [])
        austin_brew.beers = [coors_light]
        db.session.commit()

        self.assertEqual(austin_brew.beers[0].name, "Coors Light")

    def test_relationship_2(self) :
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.drop_all()
        db.create_all()

        coors_light = Beer(name='Coors Light', description="Taste's like urine.",
            is_organic="N", abv=11.1, ibu=30)
        blue_moon = Beer(name='Blue Moon', description="Pretty good.",
            is_organic="N", abv=6.3, ibu=50)
        light_lager = Style(name="Light Hail Lager")

        self.assertEqual(light_lager.beers, [])
        light_lager.beers = [coors_light, blue_moon]
        db.session.add(blue_moon)
        db.session.add(coors_light)
        db.session.add(light_lager)

        self.assertEqual(light_lager.beers[0], coors_light)
        self.assertEqual(light_lager.beers[1], blue_moon)
        self.assertEqual(light_lager.style_id, blue_moon.style_id)

        db.session.commit()


if __name__ == '__main__':
	main()

def run_tests() :
    main()
