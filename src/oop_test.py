import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric, Date, DateTime, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()

############################################################################
# Classes of data that we can directly get with the requests to api_kinohod#
############################################################################

class NetworksInfo(Base):
    __tablename__ = 'networksinfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    network_id = Column(String, nullable=False)
    title = Column(String)
    isSale = Column(Boolean)

    cinemas = relationship("Cinemas", backref='networksinfo')


class Cinemas(Base):
    __tablename__ = 'cinemas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer, nullable=False)
    title = Column(String)
    shortTitle = Column(String)
    description = Column(String)
    website = Column(String)
    city_id = Column(Integer, ForeignKey('cities.city_id'))
    address = Column(String)
    location = Column(String, ForeignKey('locations.cinema_id'))
    networkId = Column(Integer, ForeignKey('networksinfo.network_id'))
    isSale = Column(Boolean)
    mall = Column(String)
    timeToRefund = Column(Integer)
    hallCount = Column(Integer)
    subwayStations = Column(String)
    goodies = Column(String)
    photo = Column(String, ForeignKey('images.cinema_id'))
    phones = Column(String, ForeignKey('phones.cinema_id'))

    halls = relationship('Halls', backref="cinemas")


class Halls(Base):
    __tablename__ = 'halls'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hall_id = Column(Integer, nullable=False)
    cinemaId = Column(Integer, ForeignKey('cinemas.cinema_id'))
    title = Column(String)
    description = Column(String)
    placeCount = Column(Integer)
    isVIP = Column(Boolean)
    isIMAX = Column(Boolean)
    orderScanner = Column(Boolean)
    ticketScanner = Column(Boolean)


class MovieInfo(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, nullable=False)
    title = Column(String)
    duration = Column(Integer)
    originalTitle = Column(String)
    productionYear = Column(Integer)
    premiereDateRussia = Column(Date)
    premiereDateWorld = Column(Date)
    budget = Column(Numeric)
    countries = Column(String)
    producers = Column(String)
    companies = Column(String)
    directors = Column(String)
    actors = Column(String)
    genres = Column(String)
    annotationShort = Column(String)
    annotationFull = Column(String)
    ageRestriction = Column(String)
    grossRevenueRus = Column(Numeric)
    grossRevenueWorld = Column(Numeric)
    trailers = Column(String, ForeignKey('videos.trailer_id'))
    images_1 = Column(String, ForeignKey('images.image_movie_id'))
    rating = Column(Numeric)
    imdbId = Column(String)
    externalTrailer = Column(String)
    poster = Column(Integer, ForeignKey('images.poster_movie_id'))
    posterLandscape = Column(Integer, ForeignKey('images.poster_land_movie_id'))
    countScreens = Column(Integer)
    countVotes = Column(Integer)
    countComments = Column(Integer)
    weight = Column(Integer)
    isDolbyAtmos = Column(Boolean)
    isImax = Column(Boolean)
    is4dx = Column(Boolean)
    isPresale = Column(Boolean)
    distributorId = Column(Integer, ForeignKey('distributors.distributor_id'))

    images_ids = relationship("Images", foreign_keys=[images_1])
    poster_id = relationship("Images", foreign_keys=[poster])
    poster_land_id = relationship("Images", foreign_keys=[posterLandscape])



class SeanceInfo(Base):
    __tablename__ = 'seances'
    id = Column(Integer, primary_key=True, autoincrement=True)
    seance_id = Column(Integer, nullable=False)
    movieId = Column(Integer, ForeignKey('movies.id'))
    cinemaId = Column(Integer, ForeignKey('cinemas.id'))
    date = Column(DateTime)
    time = Column(DateTime)
    startTime = Column(DateTime)
    hallId = Column(Integer, ForeignKey('halls.id'))
    formats = Column(String, ForeignKey('seance_format.seance_id'))
    isSaleAllowed = Column(Boolean)
    minPrice = Column(Numeric)
    maxPrice = Column(Numeric)
    maxSeatsInOrder = Column(Integer)
    subtitleId = Column(Integer)
    languageId = Column(Integer, ForeignKey('languages.id'))
    groupName = Column(String)
    groupOrder = Column(Integer)


class CityInfo(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, nullable=False)
    title = Column(String)
    alias = Column(String)
    utcOffset = Column(Integer)
    location = Column(Integer, ForeignKey('locations.city_id'))

    cinemas = relationship("Cinemas", backref="cities")
    subwaystation = relationship("SubwayInfo", backref="cities")


class SubwayInfo(Base):
    __tablename__ = 'subwaystations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    subway_id = Column(Integer, nullable=False)
    title = Column(String)
    line = Column(String)
    color = Column(String)
    location = Column(Integer, ForeignKey('locations.subway_id'))
    city_id = Column(Integer, ForeignKey('cities.city_id'))

    cinemas = relationship("Cinemas",
                           secondary='subwaystations_cinemas',
                           backref="subways")


class Genres(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, autoincrement=True)
    genre_id = Column(String, nullable=False)
    genre_name = Column(String)
    movies = relationship("MovieInfo",
                          secondary="movies_genres",
                          backref="genr")


class Distributors(Base):
    __tablename__ = 'distributors'
    distributor_id = Column(Integer, primary_key=True, nullable=False)
    distributor_name = Column(String)
    movies = relationship("MovieInfo", backref="distributors")


class LanguageInfo(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    language_id = Column(String, nullable=False)
    title = Column(String)
    prepTitle = Column(String)
    origTitle = Column(String)
    shortTitle = Column(String)
    greeting = Column(String)


class Sources(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer, nullable=False)
    description = Column(String)

    sourceentity = relationship("SourceEntityInfo", backref="sources")


class SourceEntityInfo(Base):
    __tablename__ = 'sourceentityinfo'
    id = Column(Integer, primary_key=True, autoincrement=True)

    sourceid = Column(Integer, ForeignKey('sources.id'))


##########################################################################
#Classes of creating tables with data, that we should construct without #
#direct request to API                                                   #
##########################################################################

class CommonDicts:
    id = Column(Integer, primary_key=True, autoincrement=True)
    field_id = Column(Integer, nullable=False)
    name = Column(String)


class MyCompanies(CommonDicts, Base):
    __tablename__ = 'companies'
    movies = relationship("MovieInfo",
                          secondary="movies_companies",
                          backref="company")


class MyActors(CommonDicts, Base):
    __tablename__ = 'actors'
    movies = relationship("MovieInfo",
                          secondary="movies_actors",
                          backref="actor")


class MyProducers(CommonDicts, Base):
    __tablename__ = 'producers'
    movies = relationship("MovieInfo",
                          secondary="movies_producers",
                          backref="producer")


class MyDirectors(CommonDicts, Base):
    __tablename__ = 'directors'
    movies = relationship("MovieInfo",
                          secondary="movies_directors",
                          backref="director")


class Goodies(Base):
    __tablename__ = 'goodies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    good_title = Column(String, nullable=False)
    name = Column(String)
    cinema = relationship("Cinemas",
                          secondary="goodies_cinema",
                          backref="good")


class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)
    cinema_id = Column(Integer)
    city_id = Column(Integer)
    subway_id = Column(Integer)

    cinemas = relationship("Cinemas", backref="location_cinema")
    cities = relationship("CityInfo", backref="location_city")
    subways = relationship("SubwayInfo", backref="location_subway")



class Images(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rgb = Column(String, nullable=False)
    name = Column(String, nullable=False)
    cinema_id = Column(Integer)
    movie_id = Column(Integer)
    poster_land_movie_id = Column(Integer)
    poster_movie_id = Column(Integer)
    image_movie_id = Column(Integer)
    preview_trailer_id = Column(Integer)
    source_trailer_id = Column(Integer)
    video_id = Column(Integer)

    cinemas = relationship("Cinemas", backref="images")
    videos = relationship("Videos",
                          backref="images_videos")




class Videos(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(Integer, ForeignKey('images.video_id'))
    duration = Column(Numeric)
    contentType = Column(String)
    trailer_source = Column(Integer)
    trailer_id = Column(Integer)


##перенести##

####################################################
#associations tables for many-to-many relationships#
####################################################


class MoviesActors(Base):
    __tablename__ = 'movies_actors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    field_id = Column(Integer, ForeignKey('actors.field_id'))


class MoviesProducers(Base):
    __tablename__ = 'movies_producers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    field_id = Column(Integer, ForeignKey('producers.field_id'))


class MoviesDirectors(Base):
    __tablename__ = 'movies_directors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    field_id = Column(Integer, ForeignKey('directors.field_id'))


class MoviesCompanies(Base):
    __tablename__ = 'movies_companies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    field_id = Column(Integer, ForeignKey('companies.field_id'))


class MoviesCountries(Base):
    __tablename__ = 'movies_countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    country = Column(String)


class MoviesGenres(Base):
    __tablename__ = 'movies_genres'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    field_id = Column(Integer, ForeignKey('genres.genre_id'))


class CinemaGoodies(Base):
    __tablename__ = 'goodies_cinema'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'))
    good_title = Column(String, ForeignKey('goodies.good_title'))


class PhoneInfo(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer)
    number = Column(String)
    description = Column(String)

    cinemas = relationship("Cinemas", backref="phone")


class SubwaystationsCinemas(Base):
    __tablename__ = 'subwaystations_cinemas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'))
    subwayId = Column(Integer, ForeignKey('subwaystations.subway_id'))
    distance = Column(Integer)


class PhotosCinemas(Base):
    __tablename__ = 'photos_cinemas'
    id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey('cinemas.id'))
    rgb = Column(String)
    name = Column(String)


class Format(Base):
    __tablename__ = 'formats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    format_name = Column(String)
    description = Column(String)



class SeanceFormat(Base):
    __tablename__ = 'seance_format'
    id = Column(Integer, primary_key=True)
    seance_id = Column(Integer)
    format_name = Column(String)
    seance = relationship("SeanceInfo", backref='seances')


engine = create_engine('sqlite:///../data/oop_test2.db', encoding='utf-8')

Base.metadata.create_all(engine)
