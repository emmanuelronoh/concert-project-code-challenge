# Concerts Project

## Overview
This project manages a concert system with bands, venues, and concerts using SQLAlchemy.

## Setup

### Install Dependencies
```bash
pip install -r requirements.txt
Initialize the Database
Run the app.py script to create the database and tables:

bash
Copy code
python app.py
Usage
Create a Band
python
Copy code
band = create_band(session, "Band Name", "Hometown")
Create a Venue
python
Copy code
venue = create_venue(session, "Venue Title", "City")
Create a Concert
python
Copy code
concert = create_concert(session, band, venue, "2024-08-30")
List All Bands
python
Copy code
bands = list_bands(session)
List All Venues
python
Copy code
venues = list_venues(session)
List All Concerts
python
Copy code
concerts = list_concerts(session)
Files
models.py: Contains SQLAlchemy model definitions.
app.py: Main script for database operations.
