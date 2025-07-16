import React, { useState, useEffect } from "react";
import { uploadFile, getPrompts, analyze } from "./api";

function App() {
  const [file, setFile] = useState();
  const [fileId, setFileId] = useState();
  const [stage, setStage] = useState();
  const [progress, setProgress] = useState(0);
  const [prompts, setPrompts] = useState([]);
  const [selPrompt, setSelPrompt] = useState();
  const [resp, setResp] = useState();

  useEffect(() => {
    getPrompts().then(r => setPrompts(r.data));
  }, []);

  function onUpload() {
    uploadFile(file).then(r => {
      setFileId(r.data.file_id);
      const es = new EventSource(`${process.env.REACT_APP_API_URL}/stream/${r.data.file_id}`);
      es.onmessage = e => {
        const d = JSON.parse(e.data);
        setProgress(d.progress);
        setStage(d.stage);
        if(d.progress===100) es.close();
      };
    });
  }

  function runAnalyse() {
    analyze(fileId, selPrompt).then(r => setResp(r.data.gemini_response));
  }

  return (
    <div>
      <h1>Upload</h1>
      <input type="file" onChange={e=>setFile(e.target.files[0])} />
      <button onClick={onUpload}>Upload</button>
      <div>{stage} — {progress}%</div>

      <h1>Analyze</h1>
      <select onChange={e=>setSelPrompt(e.target.value)}>
        <option>--</option>
        {prompts.map(p=><option key={p.id} value={p.id}>{p.name}</option>)}
      </select>
      <button onClick={runAnalyse}>Run</button>
      <pre>{resp}</pre>
    </div>
  );
}

export default App;
