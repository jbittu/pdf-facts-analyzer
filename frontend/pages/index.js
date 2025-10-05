import React, { useState } from 'react'
import Results from '../components/Results'

export default function Home() {
  const [file, setFile] = useState(null)
  const [pointersText, setPointersText] = useState('List all dates\nWho signed?\nTotal contract value?')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)

  const submit = async (e) => {
    e.preventDefault()
    if (!file) return alert('Please pick a PDF file')
    const pointers = pointersText.split('\n').map(s => s.trim()).filter(Boolean)
    const form = new FormData()
    form.append('pdf', file)
    form.append('pointers', JSON.stringify(pointers))

    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: form
      })
      const data = await res.json()
      setResults(data)
    } catch (err) {
      console.error(err)
      alert('Error calling backend')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{padding: 24, maxWidth: 900, margin: '0 auto'}}>
      <h1>PDF Facts Analyzer</h1>
      <form onSubmit={submit}>
        <div>
          <label>PDF file</label><br/>
          <input type="file" accept="application/pdf" onChange={e=>setFile(e.target.files[0])} />
        </div>
        <div style={{marginTop:12}}>
          <label>Pointers (one per line)</label><br/>
          <textarea rows={6} style={{width:'100%'}} value={pointersText} onChange={e=>setPointersText(e.target.value)} />
        </div>
        <div style={{marginTop:12}}>
          <button type="submit" disabled={loading}>{loading ? 'Analyzing...' : 'Analyze'}</button>
        </div>
      </form>

      {results && <Results results={results} />}
    </div>
  )
}