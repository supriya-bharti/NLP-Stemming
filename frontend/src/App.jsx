import { useState } from "react";
import "./App.css";

function App() {
  const [showSteps, setShowSteps] = useState(false);
  const [text, setText] = useState("");
  const [operation, setOperation] = useState("both");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [evaluation, setEvaluation] = useState(null);
  const [evaluationLoading, setEvaluationLoading] = useState(false);
  const [evaluationError, setEvaluationError] = useState("");
  const [lemmaPOS, setLemmaPOS] = useState("n");
  const [lemmaEvaluation, setLemmaEvaluation] = useState(null);
  const [lemmaEvaluationLoading, setLemmaEvaluationLoading] = useState(false);
  const [lemmaEvaluationError, setLemmaEvaluationError] = useState("");

  const [preprocessingSteps, setPreprocessingSteps] = useState([]);

  function handleDownloadCSV() {
    const headers = ["Original Word"];

    if (operation !== "lemmatization") {
      headers.push("Stem");
    }

    if (operation !== "stemming") {
      headers.push("Lemma");
    }

    if (operation === "both") {
      headers.push("Transformation");
    }

    const rows = results.map((item) => {
      const row = [item.word];

      if (operation !== "lemmatization") {
        row.push(item.stem);
      }

      if (operation !== "stemming") {
        row.push(item.lemma);
      }

      if (operation === "both") {
        row.push(
          item.stem !== item.lemma ? "Stem differs from lemma" : "Same result",
        );
      }

      return row;
    });

    const csvContent = [headers, ...rows]
      .map((row) =>
        row
          .map((value) => `"${String(value ?? "").replace(/"/g, '""')}"`)
          .join(","),
      )
      .join("\n");

    const blob = new Blob([csvContent], {
      type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "nlp_analysis_results.csv";
    link.click();

    URL.revokeObjectURL(url);
  }

  async function handleEvaluate() {
    if (!text.trim()) {
      setEvaluationError("Please enter some text first.");
      setEvaluation(null);
      return;
    }

    setEvaluationLoading(true);
    setEvaluationError("");
    setEvaluation(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/evaluate/stemming", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();

      if (!response.ok || data.error) {
        throw new Error(data.error || "Evaluation failed.");
      }

      setEvaluation(data);
    } catch (err) {
      setEvaluationError(err.message || "Could not connect to the backend.");
    } finally {
      setEvaluationLoading(false);
    }
  }
  async function handleLemmaEvaluate() {
    if (!text.trim()) {
      setLemmaEvaluationError("Please enter some text first.");
      setLemmaEvaluation(null);
      return;
    }

    setLemmaEvaluationLoading(true);
    setLemmaEvaluationError("");
    setLemmaEvaluation(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/evaluate/lemmatization",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: text,
            pos: lemmaPOS,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok || data.error) {
        throw new Error(data.error || "Lemmatization evaluation failed.");
      }

      setLemmaEvaluation(data);
    } catch (err) {
      setLemmaEvaluationError(
        err.message || "Could not connect to the backend.",
      );
    } finally {
      setLemmaEvaluationLoading(false);
    }
  }
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
        body: JSON.stringify({
          text,
          operation,
          show_steps: true,
        }),
      });

      const data = await response.json();

      if (!response.ok || data.error) {
        throw new Error(data.error || "Something went wrong.");
      }

      setResults(data.results);
      setPreprocessingSteps(data.preprocessing_steps || []);
    } catch (err) {
      setError(
        err.message || "Could not connect to the backend. Is FastAPI running?",
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
            Enter a sentence and see how stemming and lemmatization transform
            its words.
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
          <p className="word-count">
            Input words: {text.trim() ? text.trim().split(/\s+/).length : 0}
          </p>

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
          <select
            value={lemmaPOS}
            onChange={(e) => setLemmaPOS(e.target.value)}
            className="operation-select"
          >
            <option value="n">Noun</option>
            <option value="v">Verb</option>
            <option value="a">Adjective</option>
          </select>

          <div className="button-group">
            <button onClick={handleProcess} disabled={loading}>
              {loading ? "Processing..." : "Analyze Text"}
            </button>

            <button
              className="clear-button"
              onClick={() => {
                setText("");
                setResults([]);
                setError("");
              }}
              disabled={loading}
            >
              Clear
            </button>
            <button
              className="steps-button"
              onClick={handleEvaluate}
              disabled={evaluationLoading}
            >
              {evaluationLoading ? "Evaluating..." : "Evaluate Stemmer"}
            </button>
            <button
              className="steps-button"
              onClick={handleLemmaEvaluate}
              disabled={lemmaEvaluationLoading}
            >
              {lemmaEvaluationLoading ? "Evaluating..." : "Evaluate Lemmatizer"}
            </button>
          </div>
        </section>
        <button
          className="steps-button"
          onClick={() => setShowSteps(!showSteps)}
        >
          {showSteps ? "Hide Preprocessing Steps" : "Show Preprocessing Steps"}
        </button>

        {showSteps && (
          <section className="panel">
            <h2>Preprocessing Steps</h2>

            {preprocessingSteps.length === 0 ? (
              <p>No preprocessing steps received. Check the backend.</p>
            ) : (
              preprocessingSteps.map((step, index) => (
                <div key={index} className="step-item">
                  <h3>
                    {index + 1}. {step.name}
                  </h3>

                  <pre>
                    {Array.isArray(step.value)
                      ? JSON.stringify(step.value, null, 2)
                      : step.value}
                  </pre>
                </div>
              ))
            )}
          </section>
        )}

        {error && <p className="error">{error}</p>}

        {results.length > 0 && (
          <section className="panel results">
            <h2>Analysis Results</h2>

            <div className="stats-grid">
              <div className="stat-card">
                <h3>Total Words</h3>
                <p>{results.length}</p>
              </div>

              <div className="stat-card">
                <h3>Unique Stems</h3>
                <p>
                  {operation !== "lemmatization"
                    ? new Set(results.map((item) => item.stem)).size
                    : "—"}
                </p>
              </div>

              <div className="stat-card">
                <h3>Different Results</h3>
                <p>
                  {operation === "both"
                    ? results.filter((item) => item.stem !== item.lemma).length
                    : "—"}
                </p>
              </div>
            </div>

            <p className="result-count">
              {results.length} words after stopword removal
            </p>

            <div className="table-wrapper">
              <button className="download-button" onClick={handleDownloadCSV}>
                Download Results (CSV)
              </button>
              <table>
                <thead>
                  <tr>
                    <th>Original Word</th>
                    {operation !== "lemmatization" && <th>Stem</th>}
                    {operation !== "stemming" && <th>Lemma</th>}
                    <th>Transformation</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((item, index) => (
                    <tr key={`${item.word}-${index}`}>
                      <td>{item.word}</td>
                      {operation !== "lemmatization" && <td>{item.stem}</td>}
                      {operation !== "stemming" && <td>{item.lemma}</td>}
                      <td>
                        {operation === "both" && item.stem !== item.lemma
                          ? "Stem differs from lemma"
                          : "Same result"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {evaluationError && <p className="error">{evaluationError}</p>}

        {evaluation && (
          <section className="panel">
            <h2>Stemming Evaluation</h2>

            <div className="stats-grid">
              <div className="stat-card">
                <h3>Total Words</h3>
                <p>{evaluation.total_words}</p>
              </div>

              <div className="stat-card">
                <h3>Accuracy</h3>
                <p>{evaluation.accuracy}%</p>
              </div>
            </div>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Word</th>
                    <th>Your Stemmer</th>
                    <th>NLTK Stemmer</th>
                    <th>Status</th>
                  </tr>
                </thead>

                <tbody>
                  {evaluation.results.map((item, index) => (
                    <tr key={`${item.word}-${index}`}>
                      <td>{item.word}</td>
                      <td>{item.custom_stem}</td>
                      <td>{item.nltk_stem}</td>
                      <td>{item.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
        {lemmaEvaluationError && (
          <p className="error">{lemmaEvaluationError}</p>
        )}

        {lemmaEvaluation && (
          <section className="panel">
            <h2>Lemmatization Evaluation</h2>

            <div className="stats-grid">
              <div className="stat-card">
                <h3>Total Words</h3>
                <p>{lemmaEvaluation.total_words}</p>
              </div>

              <div className="stat-card">
                <h3>Agreement with NLTK</h3>
                <p>{lemmaEvaluation.accuracy}%</p>
              </div>
            </div>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Word</th>
                    <th>POS</th>
                    <th>Your Lemma</th>
                    <th>NLTK Lemma</th>
                    <th>Status</th>
                  </tr>
                </thead>

                <tbody>
                  {lemmaEvaluation.results.map((item, index) => (
                    <tr key={`${item.word}-${index}`}>
                      <td>{item.word}</td>
                      <td>{item.pos}</td>
                      <td>{item.custom_lemma}</td>
                      <td>{item.nltk_lemma}</td>
                      <td>{item.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </main>

      <footer>Built with React, FastAPI, and custom NLP algorithms</footer>
    </div>
  );
}

export default App;
