Back-End-Development-Songs
Environment Setup
Repository created from the provided template.
Environment initialized locally.
Python version: 3.14
Flask application configured.
REST API implemented.
API Endpoints
Method	Endpoint	Description
GET	/health	Health check
GET	/count	Count pictures
GET	/picture	Get all pictures
GET	/picture/{id}	Get picture by ID
POST	/picture	Create picture
PUT	/picture/{id}	Update picture
DELETE	/picture/{id}	Delete picture
Running the application
py app.py
Application URL: http://127.0.0.1:5001

Testing
py -m pytest -v
