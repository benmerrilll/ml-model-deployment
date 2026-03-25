from pathlib import Path

from pydantic import BaseModel, computed_field


class MLConfig(BaseModel):
    app_name: str = "ml_engineer_exam"
    model_name: str = "linear"

    @computed_field
    @property
    def repo_dir(self) -> Path:
        # Get to the repo root from this file's location
        return Path(__file__).parent.parent.parent

    @computed_field
    @property
    def data_dir(self) -> Path:
        path = self.repo_dir / "data"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @computed_field
    @property
    def log_dir(self) -> Path:
        path = self.repo_dir / "logs"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @computed_field
    @property
    def input_data_dir(self) -> Path:
        path = self.data_dir / "input_data"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @computed_field
    @property
    def model_dir(self) -> Path:
        path = self.data_dir / "models"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @computed_field
    @property
    def model_path(self) -> Path:
        return self.model_dir / f"{self.model_name}.joblib"

    @computed_field
    @property
    def prediction_dir(self) -> Path:
        path = self.data_dir / "predictions"
        path.mkdir(parents=True, exist_ok=True)
        return path

    random_state: int = 42
    learning_rate: float = None
    num_epochs: int = None
