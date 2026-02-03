from argparse import ArgumentParser
import joblib
import json
from ml_engineer_exam.prediction import run_prediction
from ml_engineer_exam.config import MLConfig
import pandas as pd


def main():

    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        '-mn', '--model_name',
        type=str,
        default='linear',
        help='Type of model to predict (linear, ridge, random_forest)'
    )
    argument_parser.add_argument(
        '-id', '--input_data',
        type=str,
        default=None,
        help='The input data file path in string JSON format. e.g. '
             '"{\"MedInc\": 1.6812, \"HouseAge\": 25.0, \"AveRooms\": 4.192200557103064, \"AveBedrms\": 1.0222841225626742, '
             '\"Population\": 1392.0, \"AveOccup\": 3.877437325905293, \"Latitude\": 36.06, \"Longitude\": -119.01}"'

    )

    args = argument_parser.parse_args()
    model_name = args.model_name

    config = MLConfig(model_name=model_name)
    data = json.loads(args.input_data)

    model = joblib.load(config.model_dir / f'{config.model_name}.joblib')

    scaler = joblib.load(config.model_dir / f'scaler.joblib') # Should be StandardScaler, not ndarray
    preds = run_prediction(
        model=model,
        data=data,
        scaler=scaler,
    )

    print("Predictions Complete!")

    data['PredictedValue'] = preds[0]

    (config.prediction_dir / f'predictions_{config.model_name}.json').write_text(json.dumps(data, indent=4))

    print(json.dumps(data))



if __name__ == '__main__':


    main()