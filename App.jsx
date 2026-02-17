import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Preview from "./components/Preview";
import Timeline from "./components/Timeline";
import UploadPanel from "./components/UploadPanel";

import { useState } from "react";

function App() {
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState("");

  return (
    <div className="app">
      <Navbar />

      <UploadPanel 
        setTranscript={setTranscript}
        setSummary={setSummary}
      />

      <div className="main-layout">
        <Sidebar transcript={transcript} summary={summary} />
        <Preview />
      </div>

      <Timeline />
    </div>
  );
}

export default App;

