# Geospatial Webapp Server

A geospatial web application developed using Python, Django, and PostgreSQL. This project provides a server-side API for managing places, leveraging PostgreSQL's PostGIS extension for geospatial data storage and querying.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)


## Introduction

This geospatial web application allows users to manage places using a server-side API. It utilizes PostgreSQL's PostGIS extension to store and query geospatial data effectively. The application provides various features for creating, updating, retrieving, and deleting places.

## Features

- Create a new place with name, description, and geographic coordinates (latitude, longitude).
- Update the details of a place, including its name, description, and coordinates.
- Retrieve a list of all places or a specific place by ID.
- Delete a place by ID.
- Find the nearest place to a given set of coordinates (latitude, longitude).

## Technologies

The geospatial web application is built using the following technologies:

- Python
- Django
- PostgreSQL (with PostGIS extension)
- Django REST Framework
- drf_spectacular (for API documentation)

## Installation

To install and set up the geospatial web application locally, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/SergiiMachulin/geospatial-webapp-server.git`
```
2. Change to the project directory: 
```bash
cd geospatial-webapp-server
``` 
3. Create a virtual environment: 
```bash 
python3 -m venv venv
```
4. Activate the virtual environment:
```bash
venv\Scripts\activate (on Windows)
source venv/bin/activate (on Linux/macOS)
```
5. Install the required dependencies: 
```bash
pip install -r requirements.txt
```
6. Set up the PostgreSQL database and configure the connection in `settings.py`:
- *Set the required environment variables in `.env` file (need to be created, see example - `.env.sample` file)*:

    POSTGRES_DB
    
    POSTGRES_USER
    
    POSTGRES_PASSWORD
    
    POSTGRES_HOST

    DJANGO_SECRET_KEY

    DJANGO_DEBUG

    DJANGO_ALLOWED_HOSTS

7. Run the database migrations: `python manage.py migrate`.
8. Start the development server: `python manage.py runserver`
9. Open your browser and visit `http://localhost:8000` to access the application.

## Usage

Once the application is up and running, you can use the server-side API to interact with the places. Here are some example API endpoints:

- `GET /api/places`: Retrieves a list of all places.
- `POST /api/places`: Creates a new place.
- `GET /api/places/{id}`: Retrieves a specific place by ID.
- `PUT /api/places/{id}`: Updates the details of a place.
- `DELETE /api/places/{id}`: Deletes a place by ID.
- `GET /api/places/nearest_place/?latitude={latitude}&longitude={longitude}`: Finds the nearest place to the given coordinates.

For detailed API documentation, refer to the [API Documentation](#api-documentation) section below.

## API Documentation

The API documentation provides detailed information about the available endpoints, request/response formats, and examples. To explore the API documentation, follow these steps:

1. Start the development server: `python manage.py runserver`
2. Open your browser and visit `http://localhost:8000/api/schema/swagger-ui/` to view the Swagger UI documentation.

