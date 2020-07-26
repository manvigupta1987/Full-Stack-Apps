from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'venues'
    __searchable__ = ["name", "city", "state", "address"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    website = db.Column(db.String(120))

    shows = db.relationship("Show", backref='venues', lazy=True)

    def to_dict(self):
        """ Returns a dictionary of venues """
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'genres': self.genres.split(','),  # convert string to list
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'website': self.website
        }

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'

    def get_venue_id_name(self):
        return {
            'id':self.id,
            'name': self.name
        }


class Artist(db.Model):
    __tablename__ = 'artists'
    __searchable__ = ["name", "city", "state"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref='artists', lazy=True)

    def to_dict(self):
        """ Returns a dictionary of artists """
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'genres': self.genres.split(','),  # convert string to list
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
        }

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'

    def get_artist_id_name(self):
        return {
            'id':self.id,
            'name': self.name
        }


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Show {}{}>'.format(self.artist_id, self.venue_id)

    def detail(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.venues.name,
            'artist_id': self.artist_id,
            'artist_name': self.artists.name,
            'artist_image_link': self.artists.image_link,
            'start_time': self.start_time
        }

    def artist_details(self):
        return {
            'artist_id': self.venue_id,
            'artist_name': self.artists.name,
            'artist_image_link': self.artists.image_link,
            'start_time': self.start_time

        }

    def venue_details(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.venues.name,
            'venue_image_link': self.venues.image_link,
            'start_time': self.start_time

        }
