"""Shared feature schema for training and serving GradePilot's model."""

PREDICTOR_FEATURES = [
    "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu",
    "Mjob", "Fjob", "reason", "guardian", "traveltime", "studytime",
    "failures", "schoolsup", "famsup", "paid", "activities", "nursery",
    "higher", "internet", "romantic", "famrel", "freetime", "goout",
    "Dalc", "Walc", "health", "absences", "G1", "G2",
]

CATEGORICAL_FEATURES = [
    "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob", "reason",
    "guardian", "schoolsup", "famsup", "paid", "activities", "nursery",
    "higher", "internet", "romantic",
]

NUMERIC_FEATURES = [
    feature for feature in PREDICTOR_FEATURES if feature not in CATEGORICAL_FEATURES
]

TARGET_COLUMN = "G3"
EXCLUDED_FEATURES = ["school"]
PASSING_GRADE = 10
