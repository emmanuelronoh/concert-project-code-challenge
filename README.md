# Concerts Project

## Overview
This project manages a concert system with bands, venues, and concerts using SQLAlchemy.

## Setup

### Install Dependencies
Install the required Python packages:
pip install -r requirements.txt
Initialize the Database
Run the app.py script to create the database and tables:

bash
Copy code
python app.py
Usage
Create a Band
Use the following code to create a band:

python
Copy code
band = create_band(session, "Band Name", "Hometown")
Create a Venue
Use the following code to create a venue:

python
Copy code
venue = create_venue(session, "Venue Title", "City")
Create a Concert
Use the following code to create a concert:

python
Copy code
concert = create_concert(session, band, venue, "2024-08-30")
List All Bands
To list all bands:

python
Copy code
bands = list_bands(session)
List All Venues
To list all venues:

python
Copy code
venues = list_venues(session)
List All Concerts
To list all concerts:

python
Copy code
concerts = list_concerts(session)
Files
models.py: Contains SQLAlchemy model definitions.
app.py: Main script for database operations.