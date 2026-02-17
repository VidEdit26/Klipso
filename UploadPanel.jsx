import { useState } from "react";

function UploadPanel({ setTranscript, setSummary }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a video first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/process-video/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setTranscript(data.transcript);
      setSummary(data.summary);
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong");
    }

    setLoading(false);
  };

  return (
    <div>
      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={handleUpload}>
        Upload & Process
      </button>

      {loading && <p>Processing...</p>}
    </div>
  );
}

export default UploadPanel;
