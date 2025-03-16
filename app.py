import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS


from dotenv import load_dotenv



load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    load_models(app)
    register_routes(app)
    helth_check(app)
    return app


def load_model(model_path, model_type='pickle'):
    """Load a model based on its type."""
    with open(model_path, 'rb') as f:
        return pickle.load(f)


def load_models(app):
    """Load all models and attach them to the app config."""
    MODEL_DIR = os.path.join(os.path.dirname(__file__), 'data')
    model_paths = {
        'random_forest': os.path.join(MODEL_DIR, 'random_forest_model.pkl'),
        'xgboost': os.path.join(MODEL_DIR, 'xgboost_model.pkl'),
    }
    app.config['MODELS'] = {
        'random_forest': load_model(model_paths['random_forest']),
        'xgboost': load_model(model_paths['xgboost']),
    }


def register_routes(app):
    """Register all API endpoints."""
    @app.route('/predict', methods=['POST'])
    def predict():
        try:
            data = request.get_json()
            required_fields = [
                'age', 'hypertension', 'heart_disease',
                'bmi', 'HbA1c_level', 'blood_glucose_level'
            ]
            # Check if all required fields are present
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Missing fields in request'}), 400

            # Prepare the feature array and DataFrame
            features = np.array([[data[field] for field in required_fields]])
            features_df = pd.DataFrame(features, columns=required_fields)

            models = app.config.get('MODELS')
            if not models:
                return jsonify({'error': 'Models not loaded.'}), 500

            predictions = {
                'random_forest': 'Diabetic' if models['random_forest'].predict(features_df)[0] == 1 else 'Not Diabetic',
                'xgboost': 'Diabetic' if models['xgboost'].predict(features_df)[0] == 1 else 'Not Diabetic',
            }
            return jsonify({'success': True, 'predictions': predictions})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

def helth_check(app):
    @app.route('/helth', methods=['GET'])
    def helth():
        try:
            return jsonify({'status': 'ok'})
        except Exception as e:
            return jsonify({'status': "server chowked"}), 400

        
        

    

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', os.getenv('PORT')))
    app.run(host='0.0.0.0', port=port, debug=True)
