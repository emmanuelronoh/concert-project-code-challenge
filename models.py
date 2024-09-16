"""
models.py

This module defines the database models for a concert management system.
It includes models for Band, Venue, and Concert, along with their relationships.
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, scoped_session, declarative_base
from sqlalchemy import func

# Create a base class for declarative models
Base = declarative_base()

# Association table for the many-to-many relationship between Band and Venue
band_venue = Table(
    'band_venue', Base.metadata,
    Column('band_id', Integer, ForeignKey('band.id'), primary_key=True),
    Column('venue_id', Integer, ForeignKey('venue.id'), primary_key=True)
)

class Band(Base):
    """
    Represents a musical band.
    """
    __tablename__ = 'band'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hometown = Column(String, nullable=False)
    
    concerts = relationship('Concert', back_populates='band')
    venues = relationship('Venue', secondary=band_venue, back_populates='bands')
     
    def play_in_venue(self, venue, date, session):
        """
        Record a concert for this band at a specific venue on a given date.
        """
        concert = Concert(venue_id=venue.id, band_id=self.id, date=date)
        session.add(concert)
        session.commit()

    def all_introductions(self):
        """
        Return a list of introduction messages for all concerts of this band.
        """
        return [concert.introduction() for concert in self.concerts]

    @classmethod
    def most_performances(cls, db_session):
        """
        Find the band with the most performances.
        """
        return db_session.query(cls).join(Concert).group_by(cls.id).\
            order_by(func.count(Concert.id).desc()).first()

class Venue(Base):
    """
    Represents a venue where concerts are held.
    """
    __tablename__ = 'venue'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    city = Column(String, nullable=False)
    
    concerts = relationship('Concert', back_populates='venue')
    bands = relationship('Band', secondary=band_venue, back_populates='venues')

    def concert_on(self, date, db_session):
        """
        Find a concert at this venue on a specific date.
        """
        return db_session.query(Concert).filter_by(venue_id=self.id, date=date).first()

    def most_frequent_band(self, db_session):
        """
        Find the band that has performed the most at this venue.
        """
        bands_counts = db_session.query(Concert.band_id, func.count(Concert.id)).\
            filter_by(venue_id=self.id).group_by(Concert.band_id).all()
        if bands_counts:
            band_id = max(bands_counts, key=lambda x: x[1])[0]
            return db_session.get(Band, band_id)
        return None

class Concert(Base):
    """
    Represents a concert event.
    """
    __tablename__ = 'concert'
    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey('band.id'), nullable=False)
    venue_id = Column(Integer, ForeignKey('venue.id'), nullable=False)
    date = Column(String, nullable=False)

    band = relationship('Band', back_populates='concerts')
    venue = relationship('Venue', back_populates='concerts')

    def hometown_show(self):
        """
        Check if the concert is in the band's hometown.
        """
        return self.venue.city == self.band.hometown

    def introduction(self):
        """
        Return an introduction message for this concert.
        """
        return (
            f"Hello {self.venue.city}!!!!! We are {self.band.name} and "
            f"we're from {self.band.hometown}"
        )

# Database setup
DATABASE_URL = 'sqlite:///concerts.db'
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

# Define data
bands_data = [
    {"name": "The Jazz", "hometown": "New York"},
    {"name": "Rock Legends", "hometown": "Los Angeles"},
    {"name": "Classical Ensemble", "hometown": "Chicago"},
    {"name": "Pop Stars", "hometown": "Miami"},
    {"name": "Blues Brothers", "hometown": "New Orleans"}
]

venues_data = [
    {"title": "The Grand Hall", "city": "New York"},
    {"title": "Rock Arena", "city": "Los Angeles"},
    {"title": "Symphony Center", "city": "Chicago"},
    {"title": "Pop Arena", "city": "Miami"},
    {"title": "Blues Club", "city": "New Orleans"}
]

concerts_data = [
    {"band_name": "The Jazz", "venue_title": "The Grand Hall", "date": "2024-10-01"},
    {"band_name": "Rock Legends", "venue_title": "Rock Arena", "date": "2024-10-05"},
    {"band_name": "Classical Ensemble", "venue_title": "Symphony Center", "date": "2024-10-10"},
    {"band_name": "Pop Stars", "venue_title": "Pop Arena", "date": "2024-10-15"},
    {"band_name": "Blues Brothers", "venue_title": "Blues Club", "date": "2024-10-20"}
]

# Populate the database
def populate_database():
    # Add bands
    bands = [Band(**data) for data in bands_data]
    session.add_all(bands)
    session.commit()
    
    # Add venues
    venues = [Venue(**data) for data in venues_data]
    session.add_all(venues)
    session.commit()
    
    # Retrieve the bands and venues from the database
    bands_dict = {band.name: band for band in session.query(Band).all()}
    venues_dict = {venue.title: venue for venue in session.query(Venue).all()}
    
    # Add concerts
    concerts = [
        Concert(
            band_id=bands_dict[concert['band_name']].id,
            venue_id=venues_dict[concert['venue_title']].id,
            date=concert['date']
        )
        for concert in concerts_data
    ]
    session.add_all(concerts)
    session.commit()

# Call the function to populate the database
populate_database()
