from argparse import ArgumentParser
from ml_engineer_exam.model import run_model
from ml_engineer_exam.config import MLConfig
from ml_engineer_exam.model.utils import HousingModel

def main():

    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        '-mn', '--model_name',
        type=str,
        default='linear',
        help='Type of model to train (linear, ridge, random_forest)'
    )

    args = argument_parser.parse_args()
    model_name = args.model_name

    config = MLConfig(model_name=model_name)

    housing_model = HousingModel(model_type=config.model_name)

    model, metrics = run_model(
        model=housing_model,
        ml_config=config,
    )

    print("Model Training Complete!")
    print(f"RMSE: {metrics['rmse']:.2f}")
    print(f"MAE: {metrics['mae']:.2f}")
    print(f"R² Score: {metrics['r2']:.4f}")

    return model, metrics


if __name__ == '__main__':


    main()