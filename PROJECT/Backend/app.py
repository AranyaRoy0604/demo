from flask import Flask, request, jsonify
import numpy as np
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})


with open("energy_prediction_model.pkl", "rb") as f:
    model = joblib.load("energy_prediction_model.pkl")
    
@app.route("/")
def home():
    return jsonify({"status": "Energy Prediction API Running"})

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not available"}), 503

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    required_fields = ["household_size", "temperature", "has_ac", "peak_usage"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        household_size = float(data["household_size"])
        temperature = float(data["temperature"])
        has_ac = int(data["has_ac"])
        peak_usage = float(data["peak_usage"])
    except ValueError:
        return jsonify({"error": "Invalid input data types"}), 400

    input_data = np.array([[household_size, temperature, has_ac, peak_usage]])
    prediction = model.predict(input_data)[0]

    return jsonify({"predicted_energy": round(float(prediction), 2)})

if __name__ == "__main__":
    app.run(debug=False, port=80)
