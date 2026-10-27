from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from feature_schema import PASSING_GRADE, PREDICTOR_FEATURES
# Minimal logging setup
APP_DIR = Path(__file__).resolve().parent

# Load the grade regression pipeline; preprocessing is bundled with the model.
try:
    grade_model = joblib.load(APP_DIR / "models" / "grade_model.pkl")
    print("Grade prediction model loaded successfully")
except Exception as e:
    print(f"Failed to load grade prediction model: {e}")
    grade_model = None

class StudentData(BaseModel):
    # Essential inputs
    age: int = 17
    studytime: int = 2 
    failures: int = 0
    absences: int = 6
    G1: int = 5  
    G2: int = 6
    
    # Dataset predictors without a school field
    sex: str = "F" 
    address: str = "U"
    famsize: str = "GT3"
    Pstatus: str = "T"
    Medu: int = 4
    Fedu: int = 4
    Mjob: str = "at_home"
    Fjob: str = "teacher"
    reason: str = "course"
    guardian: str = "mother"
    traveltime: int = 2
    schoolsup: str = "yes"
    famsup: str = "no"
    paid: str = "no"
    activities: str = "no"
    nursery: str = "yes"
    higher: str = "yes"
    internet: str = "no"
    romantic: str = "no"
    famrel: int = 4
    freetime: int = 3
    goout: int = 4
    Dalc: int = 1
    Walc: int = 1
    health: int = 3

# Initialize FastAPI app
app = FastAPI(
    title="Advanced Analytics for Educational Performance Prediction",
    description="Estimate a student's final grade from academic, study, and wellbeing indicators.",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def service_status():
    """Expose a small status response; the SvelteKit service serves the web UI."""
    return {
        "service": "GradePilot prediction API",
        "model_ready": grade_model is not None,
        "prediction_route": "/api/predict",
    }


@app.get("/predict")
@app.get("/api/predict")
async def get_input_schema():
    """Get default student data schema for input"""
    return {
        "age": 17,
        "studytime": 2,
        "failures": 0,
        "absences": 6,
        "G1": 5,
        "G2": 6,
        "sex": "F", 
        "address": "U",
        "famsize": "GT3",
        "Pstatus": "T",
        "Medu": 4,
        "Fedu": 4,
        "Mjob": "at_home",
        "Fjob": "teacher",
        "reason": "course",
        "guardian": "mother",
        "traveltime": 2,
        "schoolsup": "yes",
        "famsup": "no",
        "paid": "no",
        "activities": "no",
        "nursery": "yes",
        "higher": "yes",
        "internet": "no",
        "romantic": "no",
        "famrel": 4,
        "freetime": 3,
        "goout": 4,
        "Dalc": 1,
        "Walc": 1,
        "health": 3
    }



@app.post("/predict")
@app.post("/api/predict")
def predict_student(data: StudentData):
    """
    Predict student's final grade and classify as pass/fail
    """
    try:
        if grade_model is None:
            raise HTTPException(status_code=500, detail="Grade prediction model is not loaded")

        input_frame = pd.DataFrame([data.model_dump()])[PREDICTOR_FEATURES]
        estimated_grade = float(np.clip(grade_model.predict(input_frame)[0], 0, 20))
        final_classification = "PASS" if estimated_grade >= PASSING_GRADE else "FAIL"
        return {
            "predicted_grade": float(round(estimated_grade, 1)),
            "percentage": f"{round((estimated_grade/20)*100, 1)}%",
            "pass_fail": final_classification,
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
