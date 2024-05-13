from flask import Flask, render_template, request
from lib_version_remla import return_version
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Get the version of the library by first instantiating the class VersionUtil and then calling the get_version method
    version = return_version.VersionUtil.get_version()
    model_service_url = os.environ.get('MODEL_SERVICE_URL')
    return render_template('index.html', version=version, model_service_url=model_service_url) 

@app.route('/predict')
def predict():
    # Get the value entered in the textbox
    url = request.form.get('url', '')
    
    data = {
        "url": "hello"
    }
    
    
    # model_service_url = os.environ.get('MODEL_SERVICE_URL')
    response = requests.post('http://model-service:8080/predict', json=data)

    # Pass the value to the prediction page template
    return render_template('prediction.html', url=url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

