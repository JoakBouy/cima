from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import gunicorn
import joblib 

app = FastAPI()

# Load pretrained model
with open('cholera_disease_model_decision_tree.pkl', 'rb') as f:
    model = pickle.load(f)

# Define request body schema 
class SymptomData(BaseModel):
    full_name: str
    dehydration: str
    vomiting: str
    diarrhea: str
    abdominal_pain: str
    symptom_count: int
    phone_number: str
    note: str

# Prediction endpoint
@app.post("/predict")
async def predict_cholera(request: SymptomData):
    
    # Format input data
    input_data = [
        request.vomiting,
        request.diarrhea,
        request.abdominal_cramps, 
        request.dehydration,
        request.symptom_count,
    ]

    print(request.json) # print full request body

    # Make prediction
    prediction = model.predict([input_data])[0]
    
    # Return response
    return {"prediction": str(prediction)}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Cholera Disease Prediction API"}