import numpy as np

def run_prediction(model, data, scaler):
    """Run prediction using the trained model."""
    # Create 2D array with shape (1, n_features)
    input_data = np.array([[v for k, v in data.items()]])

    # Transform using the fitted scaler
    scaled_data = scaler.transform(input_data)

    # Make prediction
    predictions = model.predict(scaled_data)

    return predictions