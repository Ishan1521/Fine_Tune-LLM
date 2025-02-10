from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
import torch.nn.functional as F
import requests
import os
import sys
import asyncio
import uvicorn

# Initialize FastAPI
app = FastAPI()

# Load Custom Fine-Tuned Model (DistilBERT from Hugging Face)
MODEL_PATH = r"/Users/xdisse/Desktop/Exercise 3 Tech/sentiment_model"

# Check if the model folder exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ ERROR: Model path '{MODEL_PATH}' does not exist. Check your directory.")

# Load model
tokenizer = DistilBertTokenizer.from_pretrained(MODEL_PATH)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Groq API Setup for LLaMA 3
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Correct environment variable retrieval

#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 # Get from environment
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"



# Manually set API key as a backup (only for debugging)
if not GROQ_API_KEY:
    print("❌ ERROR: API Key is missing in FastAPI. Using manual key as backup.")
    GROQ_API_KEY = "your_actual_groq_api_key_here"  # ⚠️ Replace this

if not GROQ_API_KEY:
    raise ValueError("❌ ERROR: API Key is still missing. Use 'export GROQ_API_KEY=your_api_key'")


# Debugging step: Print the API key inside FastAPI
print("FastAPI GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))  # 🚀 Debugging Step



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React frontend
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Request Schema
class SentimentRequest(BaseModel):
    text: str
    model: str  # "custom" for DistilBERT, "llama" for LLaMA 3

# Function for Custom Model (DistilBERT)
def analyze_custom(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = F.softmax(logits, dim=1)
    confidence, predicted_class = torch.max(probabilities, dim=1)

    sentiment = "positive" if predicted_class.item() == 1 else "negative"
    return {"sentiment": sentiment, "confidence": round(confidence.item(), 4)}

# Function for LLaMA 3 (Groq Cloud API)
def analyze_llama(text):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
    "model": "llama3-8b-8192",  # ✅ Use correct model name
    "messages": [
        {"role": "system", "content": "You are an AI expert in sentiment analysis."},
        {"role": "user", "content": f"Analyze the sentiment of the following text: {text}"}
    ],
    "max_tokens": 100
}


    response = requests.post(GROQ_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# Define API Endpoint
@app.post("/analyze/")
async def analyze_sentiment(request: SentimentRequest):
    if request.model == "custom":
        return analyze_custom(request.text)
    elif request.model == "llama":
        return analyze_llama(request.text)
    else:
        raise HTTPException(status_code=400, detail="Invalid model choice. Use 'custom' or 'llama'.")

# Run FastAPI (for Spyder terminal)
if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    config = uvicorn.Config("app:app", host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.serve())
