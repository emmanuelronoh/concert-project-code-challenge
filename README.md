# Concerts Project

Welcome to the Concerts Project, a comprehensive system for managing bands, venues, and concerts. This application allows you to create and view bands, venues, and concerts, as well as manage your concert data efficiently. Built using SQLAlchemy, this project provides a solid foundation for handling concert-related information.

## Features
- **Band Management**: Create and view bands, including their names and hometowns.
- **Venue Management**: Create and view venues, including their titles and cities.
- **Concert Management**: Schedule and view concerts, associating them with bands and venues.
- **Data Retrieval**: List all bands, venues, and concerts.
- **Relationships**: Understand how bands and venues relate through concerts.

## Technologies Used
- **SQLAlchemy**: Python ORM for database operations.
- **SQLite**: Lightweight database for storing concert data.

## Getting Started

### Requirements
Ensure you have Python and pip installed on your machine.

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/concerts-project.git
    ```

2. Navigate to the project directory:
    ```bash
    cd concerts-project
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Initialize the database:
    ```bash
    python app.py
    ```

## Usage

### Create a Band
To create a new band, use:
```python
band = create_band(session, "Band Name", "Hometown")


