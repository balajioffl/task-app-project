import { useEffect, useState } from "react";
import "./Check.css";

function Check() {
  const [status, setStatus] = useState("Loading...");

  useEffect(() => {
    fetch("https://task-app-project-6uvh.onrender.com/api/check/")
      .then(res => res.json())
      .then(data => 
      {
        console.log(data);
        setStatus(data.status || data.msg || "No status");
      })
      .catch(() => setStatus("Backend not reachable"));
  }, []);

  return (
    <div className="check-container">
      <div className="check-card">
        <h2 className="check-title">Backend Status</h2>
        <p className="check-status">{status}</p>
      </div>
    </div>
  );
}

export default Check;
