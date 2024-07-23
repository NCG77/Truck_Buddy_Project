from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('maintenance_model.pkl')

@app.route('/predict-maintenance', methods=['POST'])
def predict_maintenance():
    data = request.get_json()

    operation_time = data.get('operation_time', 0)
    location = data.get('location', '')
    company = data.get('company', '')
    engine = data.get('engine', '')
    milage = data.get('milage', '')

    input_data = pd.DataFrame({
        'operation_time': [operation_time],
        'location': [location],
        'company': [company],
        'engine': [engine],
        'milage': [milage],
        'location_operation_time': [f"{location}_{operation_time}"]
    })

    predictions = model.predict(input_data)
    prediction = sum(predictions) / len(predictions)

    response = {
        "operation_time": operation_time,
        "location": location,
        "company": company,
        "engine": engine,
        "milage": milage,
        "maintenance_needed": bool(prediction)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
