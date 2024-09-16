from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, Band, Venue, Concert

# Database setup
DATABASE_URL = 'sqlite:///concerts.db'
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))

def create_band(session, name, hometown):
    try:
        if session.query(Band).filter_by(name=name).first():
            print(f"Band '{name}' already exists.")
            return None
        band = Band(name=name, hometown=hometown)
        session.add(band)
        session.commit()
        return band
    except Exception as e:
        session.rollback()
        print(f"Error creating band: {e}")
        return None

def create_venue(session, title, city):
    try:
        if session.query(Venue).filter_by(title=title).first():
            print(f"Venue '{title}' already exists.")
            return None
        venue = Venue(title=title, city=city)
        session.add(venue)
        session.commit()
        return venue
    except Exception as e:
        session.rollback()
        print(f"Error creating venue: {e}")
        return None

def create_concert(session, band, venue, date):
    try:
        if session.query(Concert).filter_by(band_id=band.id, venue_id=venue.id, date=date).first():
            print(f"Concert on {date} at '{venue.title}' by '{band.name}' already exists.")
            return None
        concert = Concert(band_id=band.id, venue_id=venue.id, date=date)
        session.add(concert)
        session.commit()
        return concert
    except Exception as e:
        session.rollback()
        print(f"Error creating concert: {e}")
        return None

def get_band_by_id(session, band_id):
    try:
        return session.query(Band).get(band_id)
    except Exception as e:
        print(f"Error retrieving band: {e}")
        return None

def get_venue_by_id(session, venue_id):
    try:
        return session.query(Venue).get(venue_id)
    except Exception as e:
        print(f"Error retrieving venue: {e}")
        return None

def get_concert_by_id(session, concert_id):
    try:
        return session.query(Concert).get(concert_id)
    except Exception as e:
        print(f"Error retrieving concert: {e}")
        return None

def list_bands(session):
    try:
        return session.query(Band).all()
    except Exception as e:
        print(f"Error listing bands: {e}")
        return []

def list_venues(session):
    try:
        return session.query(Venue).all()
    except Exception as e:
        print(f"Error listing venues: {e}")
        return []

def list_concerts(session):
    try:
        return session.query(Concert).all()
    except Exception as e:
        print(f"Error listing concerts: {e}")
        return []

def main():
    print("Welcome to the Concert Management System!")

    session = Session()  # Start a session
    try:
        # Create and manage all instances within the same session
        band = create_band(session, "The Jazz", "Kenya")
        venue = create_venue(session, "The K1 Klub Club", "Kenya")

        if band and venue:
            # Create a concert using the same session
            concert = create_concert(session, band, venue, "2024-08-30")

            if concert:
                # Fetch the band and venue again from the session to ensure they are attached
                band = get_band_by_id(session, band.id)
                venue = get_venue_by_id(session, venue.id)

                if band and venue:
                    print(f"Band: {band.name}, Hometown: {band.hometown}")
                    print(f"Venue: {venue.title}, City: {venue.city}")
                    print(f"Concert Date: {concert.date}")

                    # List all bands, venues, and concerts
                    print("\nAll Bands:")
                    for b in list_bands(session):
                        print(f"{b.name}, {b.hometown}")

                    print("\nAll Venues:")
                    for v in list_venues(session):
                        print(f"{v.title}, {v.city}")

                    print("\nAll Concerts:")
                    for c in list_concerts(session):
                        band = get_band_by_id(session, c.band_id)
                        venue = get_venue_by_id(session, c.venue_id)
                        if band and venue:
                            print(f"Concert on {c.date} at {venue.title}, {venue.city} by {band.name}")

    finally:
        session.close()  # Properly close the session when done

if __name__ == "__main__":
    main()
