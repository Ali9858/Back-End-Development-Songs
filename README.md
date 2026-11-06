Back-End-Development-Songs
Environment Setup

Repository created from the provided coding-project-template.

Repository created from the provided template.
Environment initialized locally.
Python version: 3.14
Flask application configured.
REST API implemented.
Project Description

Back-End-Development-Songs is a Flask-based microservice that provides a REST API for managing songs and their lyrics.

The service allows users to retrieve songs, count available songs, and access individual song information.

API Endpoints
Method	Endpoint	Description
GET	/health	Health check
GET	/count	Count all songs
GET	/song	Get all songs
GET	/song/{id}	Get song by ID
POST	/song	Create a new song
PUT	/song/{id}	Update a song
DELETE	/song/{id}	Delete a song
Running the Application

Install dependencies:

bash
python -m pip install -r requirements.txt


Run the Flask application:

bash
python app.py


Application URL:

text
http://127.0.0.1:5000

Testing

Run the automated tests:

bash
python -m pytest -v

Technologies Used
Python 3.14
Flask
REST API
Pytest
JSON
Deployment

The Songs microservice can be deployed using Docker and OpenShift.

The service is designed to communicate with the Django Back-End Development Capstone application.

Author

Ali Bekdari

GitHub: https://github.com/Ali9858
