import React, { useState } from "react";
import Results from "../components/Results";


export default function Home() {
  const [file, setFile] = useState(null);
  const [pointersText, setPointersText] = useState(
    "List all dates\nWho signed?\nTotal contract value?"
  );
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please pick a PDF file");

    const pointers = pointersText
      .split("\n")
      .map((s) => s.trim())
      .filter(Boolean);

    const form = new FormData();
    form.append("pdf", file);
    form.append("pointers", JSON.stringify(pointers));

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: form,
      });
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
      alert("Error calling backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-container">
      <h1 className="title">📄 PDF Facts Analyzer</h1>

      <form className="analyze-form" onSubmit={submit}>
        <div className="form-group">
          <label>PDF File</label>
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </div>

        <div className="form-group">
          <label>Pointers (one per line)</label>
          <textarea
            rows={6}
            value={pointersText}
            onChange={(e) => setPointersText(e.target.value)}
          />
        </div>

        <button type="submit" disabled={loading} className="analyze-btn">
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {results && <Results results={results} />}
    </div>
  );
}
