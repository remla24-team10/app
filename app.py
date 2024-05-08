from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the value entered in the textbox
    url = request.form.get('url', '')
    
    # Pass the value to the prediction page template
    return render_template('prediction.html', url=url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
