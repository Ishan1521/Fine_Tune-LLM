# Fine_Tune-LLM


# 📌 Sentiment Analysis API (FastAPI + React)

This project provides a **FastAPI-based Sentiment Analysis API** with a **React frontend**. The backend supports two models:
- **Custom Model (DistilBERT)** → Returns structured JSON data.
- **LLaMA 3 (Groq API)** → Returns plain text responses.

## 🚀 Installation & Setup

### ** 1. Install Dependencies**
#### **Backend (FastAPI) Setup**
Make sure you have Python installed, then install the required dependencies:
```bash
pip install -r requirements.txt
```

#### **Frontend (React) Setup**
Make sure you have Node.js installed, then install dependencies:
```bash
cd frontend
npm install
```

---

### ** 2. Run FastAPI Locally**
Run the FastAPI backend with:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
If you're on **Windows**, you might need:
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```


---

### ** 3. Run React Frontend Locally**

```
Open React in your browser: [http://localhost:3000](http://localhost:3000)

---

## 📡 **Using the API Endpoints**

### ** 1 Analyze Sentiment** (`POST /analyze/`)
#### **Request:**
```json
{
  "text": "I love this movie!",
  "model": "custom"  // Options: "custom" (DistilBERT) or "llama" (LLaMA 3)
}
```
#### **Response (Custom Model - JSON)**:
```json
{
  "sentiment": "positive",
  "confidence": 0.9954
}
```
#### **Response (LLaMA Model - Plain Text)**:
```
A straightforward one!
The sentiment of the text "I love this movie!" is POSITIVE.
```

---




