//Step 11
import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [text, setText] = useState("");
  const [model, setModel] = useState("custom");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Ensure the API URL is correct
  const API_URL = "http://127.0.0.1:8000/analyze/";

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setResult(null); // Clear previous results

    try {
      console.log(`🔍 Sending request to API: ${API_URL}`);

      const response = await axios.post(API_URL, {
        text: text,
        model: model,
      });

      console.log("✅ Response from API:", response.data);

      // Handle different response formats (JSON for "custom", plain text for "llama")
      if (typeof response.data === "string") {
        setResult({ text: response.data }); // Store response as text
      } else {
        setResult(response.data); // Store as JSON for custom model
      }
    } catch (err) {
      console.error("❌ API Error:", err);

      if (err.response) {
        setError(`Server Error: ${err.response.status} - ${err.response.data.detail}`);
      } else if (err.request) {
        setError("No response from the API. Make sure FastAPI is running.");
      } else {
        setError(`Unexpected error: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center p-10 min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Sentiment Analysis</h1>

      {/* Text Input */}
      <textarea
        className="w-96 p-2 border rounded mb-4"
        placeholder="Enter text to analyze..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      {/* Model Selection Dropdown */}
      <select
        className="w-96 p-2 border rounded mb-4"
        value={model}
        onChange={(e) => setModel(e.target.value)}
      >
        <option value="custom">Custom Model</option>
        <option value="llama">Llama 3</option>
      </select>

      {/* Analyze Button */}
      <button
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        onClick={handleAnalyze}
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze Sentiment"}
      </button>

      {/* Error Display */}
      {error && <p className="text-red-500 mt-4">{error}</p>}

      {/* Result Display */}
      {result && (
        <div className="mt-6 p-4 w-96 bg-white shadow-md rounded">
          <h2 className="text-lg font-semibold">Analysis Result</h2>
          
          {/* Handle JSON response for "custom" model */}
          {result.sentiment && (
            <>
              <p className="mt-2">
                <strong>Sentiment:</strong> {result.sentiment}
              </p>
              {result.confidence !== undefined && (
                <p>
                  <strong>Confidence:</strong> {result.confidence}
                </p>
              )}
            </>
          )}

          {/* Handle plain text response for "llama" model */}
          {result.text && (
            <p className="mt-2">
              <strong>Full Response:</strong> {result.text}
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default App;
