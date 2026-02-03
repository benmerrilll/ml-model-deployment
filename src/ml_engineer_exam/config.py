from pydantic import BaseModel
from pathlib import Path


class MLConfig(BaseModel):

    app_name: str = 'ml_engineer_exam'
    model_name: str = 'linear'

    root_path: Path = Path.home() / 'Milliman'
    app_dir: Path = root_path / f'app/{app_name}'
    app_dir.mkdir(parents=True, exist_ok=True)

    data_dir: Path = root_path / f'data/{app_name}'
    data_dir.mkdir(parents=True, exist_ok=True)

    input_data_dir: Path = data_dir / 'input_data'
    input_data_dir.mkdir(parents=True, exist_ok=True)

    model_dir: Path = data_dir / 'models'
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path: Path = model_dir / f'{model_name}.joblib'

    prediction_dir: Path = data_dir / 'predictions'
    prediction_dir.mkdir(parents=True, exist_ok=True)

    random_state: int = 42
    learning_rate: float = None
    num_epochs: int = None