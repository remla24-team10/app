from flask import Flask, render_template, request, Response
from lib_version_remla import return_version
import os
import requests

app = Flask(__name__)
count_index = 0
count_predictions = 0
phishing_count = 0
probability_sum = 0

@app.route('/')
def index():
    # Get the version of the library by first instantiating the class VersionUtil and then calling the get_version method
    global count_index
    count_index += 1
    version = return_version.VersionUtil.get_version()
    model_service_url = os.environ.get('MODEL_SERVICE_URL')
    return render_template('index.html', version=version, model_service_url=model_service_url) 

@app.route('/predict', methods=['POST'])
def predict():
    # Get the value entered in the textbox
    global count_predictions, phishing_count, probability_sum
    count_predictions += 1
    url = request.form.get('url', '')
    
    data = {
        "url": url
    }    
    
    model_service_url = os.environ.get('MODEL_SERVICE_URL')
    response = requests.post(model_service_url, json=data)
    # Assuming response contains prediction results
    prediction_result = response.json()
    if(str(prediction_result['result'])== 'phishing'):
        phishing_count += 1
    probability_sum += float(prediction_result['probability'][0])

    # Pass the value to the prediction page template
    return render_template('prediction.html', url=url, prediction_result=prediction_result)


@app.route('/metrics', methods=['GET'])
def metrics():
    global count_index, count_predictions, probability_sum, phishing_count
    
    m = "# HELP Average rate of phishing requests.\n"
    m += "# TYPE phishing gauge\n"
    m += "average_phishing {}\n".format(min(1.0, phishing_count) if count_predictions == 0 else (phishing_count*1.0)/(count_predictions*1.0))
    
    m += "# HELP probability Average prediction score with 0 being legitimate and 1 being phishing.\n"
    m += "# TYPE probability gauge\n"
    m += "average_probability {}\n".format(min(1.0, probability_sum) if count_predictions == 0 else probability_sum/count_predictions*1.0)

    m += "# HELP num_requests The number of requests that have been served, by page.\n"
    m += "# TYPE num_requests counter\n"
    m += "num_requests{{page=\"index\"}} {}\n".format(count_index)
    m += "num_requests{{page=\"predict\"}} {}\n\n".format(count_predictions)
    
    return Response(m, mimetype="text/plain")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

