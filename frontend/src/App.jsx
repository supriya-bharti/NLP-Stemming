
import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [operation, setOperation] = useState("both");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleProcess() {
    if (!text.trim()) {
      setError("Please enter some text first.");
      setResults([]);
      return;
    }

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text, operation }),
      });

      const data = await response.json();

      if (!response.ok || data.error) {
        throw new Error(data.error || "Something went wrong.");
      }

      setResults(data.results);
    } catch (err) {
      setError(
        err.message || "Could not connect to the backend. Is FastAPI running?"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">NLP</div>
        <div>
          <h1>Text Analyzer</h1>
          <p>Stemming and Lemmatization System</p>
        </div>
      </header>

      <main className="container">
        <section className="intro">
          <h2>Explore your text</h2>
          <p>
            Enter a sentence and see how stemming and lemmatization
            transform its words.
          </p>
        </section>

        <section className="panel">
          <label htmlFor="text">Your text</label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Example: The students are studying natural language processing..."
            rows={5}
          />

          <label htmlFor="operation">Choose an operation</label>
          <select
            id="operation"
            value={operation}
            onChange={(e) => setOperation(e.target.value)}
          >
            <option value="stemming">Stemming only</option>
            <option value="lemmatization">Lemmatization only</option>
            <option value="both">Both operations</option>
          </select>

          <button onClick={handleProcess} disabled={loading}>
            {loading ? "Processing..." : "Analyze Text"}
          </button>
        </section>

        {error && <p className="error">{error}</p>}

        {results.length > 0 && (
          <section className="panel results">
            <h2>Analysis Results</h2>
            <p className="result-count">
              {results.length} words after stopword removal
            </p>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Original Word</th>
                    {operation !== "lemmatization" && <th>Stem</th>}
                    {operation !== "stemming" && <th>Lemma</th>}
                  </tr>
                </thead>
                <tbody>
                  {results.map((item, index) => (
                    <tr key={`${item.word}-${index}`}>
                      <td>{item.word}</td>
                      {operation !== "lemmatization" && (
                        <td>{item.stem}</td>
                      )}
                      {operation !== "stemming" && (
                        <td>{item.lemma}</td>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </main>

      <footer>
        Built with React, FastAPI, and custom NLP algorithms
      </footer>
    </div>
  );
}

export default App;
