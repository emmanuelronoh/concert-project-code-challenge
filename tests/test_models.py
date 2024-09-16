import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, Band, Venue, Concert



# Database setup for testing
DATABASE_URL = 'sqlite:///test_concerts.db'
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))

@pytest.fixture(scope='module')
def session():
    """Fixture for creating a session for the tests."""
    session = Session()
    yield session
    session.close()
    # Drop all tables after tests
    Base.metadata.drop_all(engine)

def test_band_creation(session):
    """Test creation of a Band."""
    band = Band(name="The Jazz", hometown="Kenya")
    session.add(band)
    session.commit()
    assert band.id is not None
    # Use Session.get() instead of Query.get()
    retrieved_band = session.get(Band, band.id)
    assert retrieved_band is not None
    assert retrieved_band.name == "The Jazz"
    assert retrieved_band.hometown == "Kenya"

def test_venue_creation(session):
    """Test creation of a Venue."""
    venue = Venue(title="The K1 Klub Club", city="Kenya")
    session.add(venue)
    session.commit()
    assert venue.id is not None
    # Use Session.get() instead of Query.get()
    retrieved_venue = session.get(Venue, venue.id)
    assert retrieved_venue is not None
    assert retrieved_venue.title == "The K1 Klub Club"
    assert retrieved_venue.city == "Kenya"

def test_concert_creation(session):
    """Test creation of a Concert and relationships."""
    band = Band(name="The Jazz", hometown="Kenya")
    venue = Venue(title="The K1 Klub Club", city="Kenya")
    session.add(band)
    session.add(venue)
    session.commit()

    concert = Concert(band_id=band.id, venue_id=venue.id, date="2024-08-30")
    session.add(concert)
    session.commit()

    assert concert.id is not None
    # Use Session.get() instead of Query.get()
    retrieved_concert = session.get(Concert, concert.id)
    assert retrieved_concert is not None
    assert retrieved_concert.band_id == band.id
    assert retrieved_concert.venue_id == venue.id
    assert retrieved_concert.date == "2024-08-30"

def test_band_play_in_venue(session):
    """Test Band's play_in_venue method."""
    band = Band(name="The Jazz", hometown="Kenya")
    venue = Venue(title="The K1 Klub Club", city="Kenya")
    session.add(band)
    session.add(venue)
    session.commit()

    band.play_in_venue(venue, "2024-08-30", session)
    concert = session.query(Concert).filter_by(band_id=band.id, venue_id=venue.id).first()
    assert concert is not None
    assert concert.date == "2024-08-30"

def test_band_all_introductions(session):
    """Test Band's all_introductions method."""
    band = Band(name="The Jazz", hometown="Kenya")
    venue = Venue(title="The K1 Klub Club", city="Kenya")
    session.add(band)
    session.add(venue)
    session.commit()

    band.play_in_venue(venue, "2024-08-30", session)
    introductions = band.all_introductions()
    expected_intro = "Hello Kenya!!!!! We are The Jazz and we're from Kenya"
    assert introductions == [expected_intro]

def test_venue_concert_on(session):
    """Test Venue's concert_on method."""
    band = Band(name="The Jazz", hometown="Kenya")
    venue = Venue(title="The K1 Klub Club", city="Kenya")
    session.add(band)
    session.add(venue)
    session.commit()

    band.play_in_venue(venue, "2024-08-30", session)
    concert = venue.concert_on("2024-08-30", session)
    assert concert is not None
    assert concert.date == "2024-08-30"

def test_band_most_performances(session):
    """Test Band's most_performances class method."""
    band1 = Band(name="The Jazz", hometown="Kenya")
    band2 = Band(name="The Rolling Stones", hometown="Uganda")
    venue = Venue(title="The K1 Klub Club", city="Kenya")
    session.add(band1)
    session.add(band2)
    session.add(venue)
    session.commit()

    band1.play_in_venue(venue, "2024-08-30", session)
    band1.play_in_venue(venue, "2024-08-16", session)
    band2.play_in_venue(venue, "2024-08-15", session)

    most_performances_band = Band.most_performances(session)
    assert most_performances_band == band1

def test_venue_most_frequent_band(session):
    """Test Venue's most_frequent_band method."""
    band1 = Band(name="The Jazz", hometown="Kenya")
    band2 = Band(name="The Rolling Stones", hometown="Uganda")
    venue = Venue(title="The K1 Klub Club", city="Kenya")
    session.add(band1)
    session.add(band2)
    session.add(venue)
    session.commit()

    band1.play_in_venue(venue, "2024-08-30", session)
    band1.play_in_venue(venue, "2024-08-16", session)
    band2.play_in_venue(venue, "2024-08-30", session)

    frequent_band = venue.most_frequent_band(session)
    assert frequent_band == band1

def test_concert_hometown_show(session):
    """Test Concert's hometown_show method."""
    band = Band(name="The Jazz", hometown="Kenya")
    venue = Venue(title="The K1 Klub Club", city="Kenya")
    session.add(band)
    session.add(venue)
    session.commit()

    concert = Concert(band_id=band.id, venue_id=venue.id, date="2024-08-30")
    session.add(concert)
    session.commit()

    assert concert.hometown_show() is True

def test_concert_introduction(session):
    """Test Concert's introduction method."""
    band = Band(name="The Jazz", hometown="Kenya")
    venue = Venue(title="The K1 Klub Club", city="Kenya")
    session.add(band)
    session.add(venue)
    session.commit()

    concert = Concert(band_id=band.id, venue_id=venue.id, date="2024-08-30")
    session.add(concert)
    session.commit()

    intro = concert.introduction()
    expected_intro = "Hello Kenya!!!!! We are The Jazz and we're from Kenya"
    assert intro == expected_intro
