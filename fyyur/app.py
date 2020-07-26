# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from forms import *
from models import db, Artist, Venue, Show

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    try:
        data = []
        # venue_list = Venue.query.outerjoin(Show, Show.venue_id == Venue.id) \
        #     .add_columns(Venue.id, Venue.city, Venue.state, Venue.name, Show.start_time, Show.artist_id) \
        #     .all()
        venue_list = Venue.query.group_by(Venue.id, Venue.state, Venue.city) \
            .add_columns(Venue.id, Venue.city, Venue.state, Venue.name) \
            .all()
        venue_state_and_city = ''
        for venue in venue_list:
            upcoming_shows = Show.query.filter(venue.id == Show.venue_id, Show.start_time > datetime.utcnow()) \
                .count()

            if venue_state_and_city == venue.city + venue.state:
                data[len(data) - 1]["venues"].append({
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": upcoming_shows
                })
            else:
                venue_state_and_city = venue.city + venue.state
                data.append({
                    "city": venue.city,
                    "state": venue.state,
                    "venues": [{
                        "id": venue.id,
                        "name": venue.name,
                        "num_upcoming_shows": upcoming_shows
                    }]
                })
        if data:
            return render_template('pages/venues.html', areas=data)
        else:
            return render_template('errors/no_item.html', message="No Venues found")
    except:
        flash('An error occurred. No venues to display currently')
        return redirect(url_for('index'))


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term')
    venue_list = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all();

    data = list(map(Venue.get_venue_id_name, venue_list))
    response = {
        "count": len(venue_list),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    seeking_description = ''
    past_show_count = 0
    upcoming_show_count = 0
    show_list = Show.query.filter_by(venue_id=venue_id) \
        .order_by(db.desc(Show.start_time)) \
        .all()

    # shows the venue page with the given venue_id
    if len(show_list):
        if show_list[0].venues.seeking_talent:
            seeking_description = "We are on the lookout for a local artist to play every two weeks. Please call us."
        data = fill_data(show_list[0].venues, seeking_description)

        for show in show_list:
            if show.start_time < datetime.utcnow():
                past_show_count = past_show_count + 1
                data["past_shows"].append({
                    "artist_id": show.artist_id,
                    "artist_name": show.artists.name,
                    "artist_image_link": show.artists.image_link,
                    "start_time": format_datetime(str(show.start_time))
                })
            else:
                upcoming_show_count = upcoming_show_count + 1
                data["upcoming_shows"].append({
                    "artist_id": show.artist_id,
                    "artist_name": show.artists.name,
                    "artist_image_link": show.artists.image_link,
                    "start_time": format_datetime(str(show.start_time))
                })
        data['past_shows_count'] = past_show_count
        data['upcoming_shows_count'] = upcoming_show_count
        data["id"] = venue_id
    else:
        venue = Venue.query.filter_by(id=venue_id).first()
        if venue.seeking_talent:
            seeking_description = "We are on the lookout for a local artist to play every two weeks. Please call us."
        data = fill_data(venue, seeking_description)
        data["id"] = venue_id
    return render_template('pages/show_venue.html', venue=data)


def fill_data(obj, seeking_description):
    return {
        "name": obj.name,
        "genres": obj.genres,
        "address": obj.address,
        "city": obj.city,
        "state": obj.state,
        "phone": obj.phone,
        "website": obj.website,
        "facebook_link": obj.facebook_link,
        "seeking_talent": obj.seeking_talent,
        "seeking_description": seeking_description,
        "image_link": obj.image_link,
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        form = VenueForm()
        venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data, address=form.address.data,
                      phone=form.phone.data, image_link=form.image_link.data, genres=form.genres.data,
                      facebook_link=form.facebook_link.data, website=form.website.data,
                      seeking_talent=bool(form.seeking_talent.data))

        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + form.name.data + ' was successfully listed!')

    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    try:
        # Get venue by ID
        venue = Venue.query.get(venue_id)
        venue_name = venue.name

        db.session.delete(venue)
        db.session.commit()

        flash('Venue ' + venue_name + ' was deleted')
    except:
        flash('an error occured and Venue ' + venue_name + ' was not deleted')
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))

    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = []
    artists_list = Artist.query.add_columns(Artist.id, Artist.name).all()
    for artist in artists_list:
        data.append({
            "id": artist.id,
            "name": artist.name
        })
    if data:
        return render_template('pages/artists.html', artists=data)
    else:
        return render_template('errors/no_item.html', message="No Artists found")


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term')
    artist_list = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()

    data = list(map(Artist.get_artist_id_name, artist_list))
    response = {
        "count": len(artist_list),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    past_show_count = 0
    upcoming_show_count = 0
    show_list = Show.query.filter_by(artist_id=artist_id) \
        .order_by(db.desc(Show.start_time)) \
        .all()

    # shows the venue page with the given venue_id
    if len(show_list):
        data = fill_artist_data(show_list[0].artists)

        for show in show_list:
            if show.start_time < datetime.utcnow():
                past_show_count = past_show_count + 1
                data["past_shows"].append({
                    "venue_id": show.venue_id,
                    "venue_name": show.venues.name,
                    "venue_image_link": show.venues.image_link,
                    "start_time": format_datetime(str(show.start_time))
                })
            else:
                upcoming_show_count = upcoming_show_count + 1
                data["upcoming_shows"].append({
                    "venue_id": show.venue_id,
                    "venue_name": show.venues.name,
                    "venue_image_link": show.venues.image_link,
                    "start_time": format_datetime(str(show.start_time))
                })
        data['past_shows_count'] = past_show_count
        data['upcoming_shows_count'] = upcoming_show_count
        data["id"] = artist_id
    else:
        artist = Artist.query.filter_by(id=artist_id).first()
        data = fill_artist_data(artist)
        data["id"] = artist_id
    return render_template('pages/show_artist.html', artist=data)


def fill_artist_data(obj):
    print(obj.seeking_venue)
    return {
        "name": obj.name,
        "genres": obj.genres,
        "city": obj.city,
        "state": obj.state,
        "phone": obj.phone,
        "website": obj.website,
        "facebook_link": obj.facebook_link,
        "seeking_venue": obj.seeking_venue,
        "seeking_description": obj.seeking_description,
        "image_link": obj.image_link,
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }
    # shows the venue page with the given venue_id


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()

    form.name.data = artist.name
    form.genres.data = artist.genres
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.website.data = artist.website
    form.facebook_link.data = artist.facebook_link
    print(artist.seeking_venue)
    form.seeking_venue.data = str(artist.seeking_venue)
    form.seeking_description.data = artist.seeking_description
    form.image_link.data = artist.image_link
    return render_template('forms/edit_artist.html', form=form, artist=artist)



@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

    # artist record with ID <artist_id> using the new attributes
    try:
        form = ArtistForm()
        artist = Artist.query.get(artist_id)
        artist.name = form.name.data
        print(form.genres.data)
        artist.genres = form.genres.data
        print(artist.genres)
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.website = form.website.data
        artist.facebook_link = form.facebook_link.data
        artist.seeking_venue = bool(form.seeking_venue.data)
        artist.seeking_description = form.seeking_description.data
        artist.image_link = form.image_link.data
        print(artist.seeking_venue)
        db.session.commit()
        flash('Artist ' + form.name.data + ' has been updated')
    except Exception as e:
        print(e)
        db.session.rollback()
        flash('An error occured while trying to update Artist')
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).first()
    if venue:
        form.name.data = venue.name
        form.genres.data = venue.genres
        form.address.data = venue.address
        form.city.data = venue.city
        form.state.data = venue.state
        form.phone.data = venue.phone
        form.website.data = venue.website
        form.facebook_link.data = venue.facebook_link
        form.seeking_talent.data = venue.seeking_talent
        form.image_link.data = venue.image_link
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # venue record with ID <venue_id> using the new attributes
    try:
        form = VenueForm()
        venue = Venue.query.filter_by(id=venue_id).first()
        venue.name = form.name.data
        venue.genres = form.genres.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.facebook_link = form.facebook_link.data
        venue.website = form.website.data
        venue.image_link = form.image_link.data
        venue.seeking_talent = form.seeking_talent.data

        db.session.commit()
        flash('Venue ' + form.name.data + ' has been updated')
    except:
        db.session.rollback()
        flash('An error occured while trying to update Venue')
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    try:
        form = ArtistForm()
        artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data,
                        phone=form.phone.data, image_link=form.image_link.data, genres=form.genres.data,
                        facebook_link=form.facebook_link.data, website=form.website.data,
                        seeking_venue=bool(form.seeking_venue.data),
                        seeking_description=form.seeking_description.data)

        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')

    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    data = []
    show_list = Show.query.order_by(db.desc(Show.start_time))
    for show in show_list:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venues.name,
            "artist_id": show.artist_id,
            "artist_name": show.artists.name,
            "artist_image_link": show.artists.image_link,
            "start_time": format_datetime(str(show.start_time))
        })
    if data:
        return render_template('pages/shows.html', shows=data)
    else:
        return render_template('errors/no_item.html', message='No Shows are found currently')


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    try:
        form = ShowForm()
        show = Show(artist_id=form.artist_id.data, venue_id=form.venue_id.data,
                    start_time=form.start_time.data)

        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')

    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
