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
python app.py
Usage
Create a Band
python
band = create_band(session, "Band Name", "Hometown")
Create a Venue
python
venue = create_venue(session, "Venue Title", "City")
Create a Concert
python
concert = create_concert(session, band, venue, "2024-08-30")
List All Bands
python
bands = list_bands(session)
List All Venues
python
venues = list_venues(session)
List All Concerts
python
concerts = list_concerts(session)
Files
models.py: Contains SQLAlchemy model definitions.
app.py: Main script for database operations.
