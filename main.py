from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib

app = FastAPI(title="Spam Mail Detection API")

# Load model pipeline
# We use a try-except block so the app can start even if the model isn't built yet,
# though it will fail when predicting.
try:
    model_pipeline = joblib.load("spam_model.pkl")
    print("Model loaded successfully.")
except Exception as e:
    print(f"Warning: Model could not be loaded: {e}")
    model_pipeline = None

# Input schema
class MessageData(BaseModel):
    message: str

# Serve the static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")

@app.post("/predict")
def predict_spam(data: MessageData):
    if not model_pipeline:
        return {"error": "Model not loaded. Please run train_model.py first."}
    
    # The pipeline expects a list/array of strings
    prediction = model_pipeline.predict([data.message])[0]
    
    # In our trained model, 1 is spam and 0 is ham
    result = "Spam" if prediction == 1 else "Ham"
    return {"prediction": result}
