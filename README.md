# App
This application uses model services after a query of the user to display the results of querying the phising-detection model. 

## Running the app in a docker container
1. ```docker build . -t flask_app``` 
2. ```docker run -p 5000:5000 flask_app```
You can then access the web app at http://localhost:5000 in your browser. 

## Dependencies
- Flask
- Docker
- Poetry 
- Python 3.11

## Functionality requirements for assignment A2
- Depends on the lib-version through a package manager (e.g., Maven). The version is visible in the frontend.
- Queries the model-service through REST requests.
- The URL of the model-service is configurable as an environment variable.