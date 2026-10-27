"""Train and save GradePilot's grade-prediction model from the supplied datasets."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from feature_schema import (
    CATEGORICAL_FEATURES,
    EXCLUDED_FEATURES,
    PASSING_GRADE,
    PREDICTOR_FEATURES,
    TARGET_COLUMN,
)

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "datasets"
MODEL_DIR = APP_DIR / "models"


def load_dataset() -> tuple[pd.DataFrame, pd.Series]:
    """Combine both course datasets while excluding school from model inputs."""
    students = pd.concat(
        [
            pd.read_csv(DATA_DIR / "Maths.csv"),
            pd.read_csv(DATA_DIR / "Portuguese.csv"),
        ],
        ignore_index=True,
    )
    predictors = students.drop(columns=[TARGET_COLUMN, *EXCLUDED_FEATURES])
    if list(predictors.columns) != PREDICTOR_FEATURES:
        raise ValueError("Dataset columns do not match the shared model feature schema.")
    if predictors.isna().any().any() or students[TARGET_COLUMN].isna().any():
        raise ValueError("The supplied dataset contains missing values.")
    return predictors, students[TARGET_COLUMN].astype(float)


def build_model() -> Pipeline:
    preprocessing = ColumnTransformer(
        transformers=[
            ("categories", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("numeric", "passthrough", [f for f in PREDICTOR_FEATURES if f not in CATEGORICAL_FEATURES]),
        ],
        remainder="drop",
    )
    return Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=400,
                    min_samples_leaf=2,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def train_and_save() -> dict[str, float]:
    predictors, grades = load_dataset()
    x_train, x_test, y_train, y_test = train_test_split(
        predictors, grades, test_size=0.2, random_state=42
    )
    evaluation_model = build_model()
    evaluation_model.fit(x_train, y_train)
    estimated_grades = evaluation_model.predict(x_test).clip(0, 20)
    metrics = {
        "mae": float(mean_absolute_error(y_test, estimated_grades)),
        "rmse": float(mean_squared_error(y_test, estimated_grades) ** 0.5),
        "r2": float(r2_score(y_test, estimated_grades)),
        "pass_fail_accuracy": float(
            accuracy_score(y_test >= PASSING_GRADE, estimated_grades >= PASSING_GRADE)
        ),
    }

    deployed_model = build_model()
    deployed_model.fit(predictors, grades)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_DIR / "grade_model.pkl"
    joblib.dump(deployed_model, model_path)

    print(f"Rows used: {len(predictors)}")
    print(f"Predictors used: {len(PREDICTOR_FEATURES)} (school excluded)")
    print(f"Held-out mean absolute error: {metrics['mae']:.2f} grade points")
    print(f"Held-out pass/fail accuracy: {metrics['pass_fail_accuracy']:.1%}")
    print(f"Saved model: {model_path}")
    return metrics


if __name__ == "__main__":
    train_and_save()
