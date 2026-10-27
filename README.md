# GradePilot

<p align="center">
  <img src="frontend/static/favicon.svg" alt="GradePilot logo" width="96" />
</p>

> **ITTE 105b · Analytics Application · Final Project**

GradePilot is a student performance analytics app that estimates a student's final grade and highlights signals that may help guide early academic support. Enter a student profile to see an estimated grade, a pass/fail outlook, and suggested next steps.

## Features

- Predicts a final grade on the dataset's 0–20 scale.
- Labels estimates of **10/20 or higher as PASS** and lower estimates as **FAIL**.
- Summarizes signals from recent grades, attendance, study time, and prior class failures.
- Provides practical recommendations to support student check-ins.
- Offers a responsive SvelteKit interface with light and dark themes.
- Includes a notebook and a reproducible model-training script.

Predictions are estimates for early-support conversations. They should be considered alongside educator knowledge and other relevant information.

## Technology

- **Frontend:** SvelteKit, Svelte 5, TypeScript, Tailwind CSS, Lucide icons
- **API:** FastAPI, Pydantic
- **Model:** scikit-learn `RandomForestRegressor` with a preprocessing pipeline
- **Data processing:** pandas, NumPy
- **Deployment:** Vercel Services configuration

## Run locally

### Requirements

- Python 3.12
- Node.js 22 or later and npm

### 1. Install API dependencies

From the repository root, create and activate a virtual environment in `app/`.

**Windows PowerShell**

```powershell
cd app
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**macOS / Linux**

```bash
cd app
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Start the API

Keep the virtual environment active and run this from the `app/` directory:

```bash
python -m uvicorn server:app --host 127.0.0.1 --port 8002
```

The API exposes `GET /api/predict` for its default input schema and `POST /api/predict` for a prediction. The API root (`/`) returns service status.

### 3. Start the frontend

In a second terminal, from the repository root:

```bash
cd frontend
npm ci
npm run dev
```

Open **http://127.0.0.1:8001/**. The frontend development server proxies `/api/*` requests to the API on port 8002.

## Model and data

The model estimates the dataset's `G3` final grade from 31 student, family, and study predictors. The `school` field is deliberately excluded from model inputs. The deployed pipeline preprocesses categorical inputs and fits a random forest regressor.

The training script combines the Mathematics and Portuguese student datasets, evaluates a held-out split, then fits a final model on the full data and saves it to `app/models/grade_model.pkl`.

To retrain the model, install the API dependencies and run from `app/`:

```bash
python train_models.py
```

The script reports held-out mean absolute error, RMSE, R², and pass/fail accuracy. Results can vary if the data or training configuration changes.

The dataset is available from [Kaggle's Student Performance dataset](https://www.kaggle.com/datasets/whenamancodes/student-performance). The dataset has its own attribution and license terms; see `app/README.md` for the project’s dataset note.

## Deployment

The repository's `vercel.json` routes `/api/*` to the FastAPI service and other paths to the SvelteKit frontend. See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment and local environment details.

## Repository layout

```text
.
├── app/
│   ├── datasets/          # Mathematics and Portuguese datasets
│   ├── models/            # Trained grade prediction pipeline
│   ├── assets/            # Legacy static UI files
│   ├── feature_schema.py  # Shared model feature definitions
│   ├── server.py          # FastAPI prediction API
│   ├── train_models.py    # Model training and evaluation
│   └── Untitled.ipynb     # Analysis notebook
├── frontend/
│   ├── src/               # SvelteKit application
│   ├── static/            # Static files, including the favicon
│   └── package.json
├── DEPLOYMENT.md
├── LICENSE
└── README.md
```

## Contributors

- PATAJO, Odrei John C.
- DE LEON, Queenie A.
- NOVELOZO, Racell Jay C.
- MANAHAN, John Felix R.
- OCHOCO, John Patrick B.

## License

The project code is licensed under the [MIT License](LICENSE). The student dataset is distributed under CC BY 4.0 according to the project documentation; retain its attribution when using it.
