# GradePilot: Advanced Analytics for Educational Performance Prediction

## Project Overview
GradePilot is an educational analytics application that estimates a student's final grade from academic, study, and wellbeing indicators. Its Random Forest regressor predicts the G3 final grade; the app labels estimates of 10/20 or higher as PASS. The source CSVs include a school column, but school is excluded from both model training and prediction inputs.

## Features
- Estimated final grade on a 0–20 scale and pass/fail outlook (≥10 = Pass)
- 31 dataset predictors, with school excluded
- Real-time prediction and risk assessment
- Actionable recommendations for improvement
- Interactive SvelteKit dashboard with light and dark themes
- FastAPI backend for ML inference
- Docker-ready deployment

## Folder Structure
```
app/
├── assets/           # Legacy static files; the API no longer serves these
├── datasets/         # Source data (Maths.csv, Portuguese.csv)
├── models/           # Trained grade regression pipeline
├── feature_schema.py # Shared predictor list; school is excluded
├── train_models.py   # Reproducible model training and evaluation
├── server.py         # FastAPI backend
├── requirements.txt  # Python dependencies
├── Untitled.ipynb    # Jupyter notebook (ML pipeline)
```

## Installation & Usage
1. Install the Python dependencies from `app/` with `pip install -r requirements.txt`.
2. Start the API from `app/` on port 8002: `uvicorn server:app --host 127.0.0.1 --port 8002`.
3. In a second terminal, start the SvelteKit frontend from `frontend/` on port 8001: `npm run dev -- --host 127.0.0.1 --port 8001`.
4. Open `http://127.0.0.1:8001/`. Port 8000 is left for the user's other project.

## Model Training
- Install dependencies from `requirements.txt`.
- Run `python train_models.py` from this folder.
- The script combines Maths and Portuguese data, excludes `school`, evaluates a held-out split, then saves `models/grade_model.pkl`.
- The held-out estimate is reported in grade-point MAE and pass/fail accuracy. It can differ from results in the original analysis notebook.

## Deployment
The SvelteKit frontend and FastAPI API deploy as separate Vercel Services; see the repository-level `DEPLOYMENT.md` for local and Vercel instructions. The API root returns service status; the SvelteKit service owns the application interface.

## Dataset Source
This project uses the Student Performance dataset from Kaggle:
https://www.kaggle.com/datasets/whenamancodes/student-performance

## Team Members
- PATAJO, Odrei John C.
- DE LEON, Queenie A.
- NOVELOZO, Racell Jay C.
- MANAHAN, John Felix R.
- OCHOCO, John Patrick B.

## License
This project is released under the MIT License for all code and assets.
The dataset is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0) from Kaggle.
See LICENSE file for details.

## Contact
For questions or collaboration, please open an issue or discussion on the GitHub repository:
https://github.com/Bas1CUBER/Final-Project

Or email the leaeder at:
odreip@gmail.com
