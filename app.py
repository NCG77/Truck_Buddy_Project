from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load the trained model
relative_path = "maintenance_model.pkl"
model_path = os.path.join(os.path.dirname(__file__), relative_path)
model = joblib.load(model_path)

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
        'milage': [milage]
    })

    # Create interaction features
    input_data['location_operation_time'] = input_data['location'] + '_' + input_data['operation_time'].astype(str)
    input_data['location_company'] = input_data['location'] + '_' + input_data['company']
    input_data['location_engine'] = input_data['location'] + '_' + input_data['engine']
    input_data['location_milage'] = input_data['location'] + '_' + input_data['milage'].astype(str)
    input_data['company_engine'] = input_data['company'] + '_' + input_data['engine']
    input_data['company_milage'] = input_data['company'] + '_' + input_data['milage'].astype(str)
    input_data['engine_milage'] = input_data['engine'] + '_' + input_data['milage'].astype(str)

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
