import React, { useState } from 'react'

export default function Results({ results }){
  // results: { file, results: { pointer: [matches] } }
  const [open, setOpen] = useState({})
  return (
    <div style={{marginTop:20}}>
      <h2>Results for {results.file}</h2>
      {Object.entries(results.results).map(([pointer, matches]) => (
        <div key={pointer} style={{border:'1px solid #ddd', padding:12, marginBottom:12}}>
          <h3>{pointer}</h3>
          {matches && matches.length ? (
            matches.map((m, i) => (
              <div key={i} style={{marginBottom:8}}>
                <div><strong>Page:</strong> {m.page ?? '—'}</div>
                <div><strong>Snippet:</strong> {m.snippet || '—'}</div>
                <div><strong>Offsets:</strong> {m.start_char ?? '—'} — {m.end_char ?? '—'}</div>
                <div><em>{m.rationale}</em></div>
                <details style={{marginTop:6}}>
                  <summary>Show more context</summary>
                  <pre style={{whiteSpace:'pre-wrap'}}>{m.snippet}</pre>
                </details>
              </div>
            ))
          ) : (
            <div>No matches</div>
          )}
        </div>
      ))}
    </div>
  )
}