import { useState, useEffect } from "react";
import axios from "axios";
import "./TaskForm.css";

function TaskForm({ selectedTask, onSuccess, onClose }) {

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("pending");
  const [priority, setPriority] = useState("low");
  const [duedate, setDuedate] = useState("");
  const [assignedTo, setAssignedTo] = useState("");
  const [errors, setErrors] = useState({});
  const [file, setFile] = useState(null);
  const [users, setUsers] = useState([]);

  const token = localStorage.getItem("token");

      useEffect(() => {
      axios.get("https://task-app-project-6uvh.onrender.com/api/users/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        setUsers(res.data);
      })
      .catch((err) => {
        console.log("Error fetching users", err);
      });
    }, [token]);

  useEffect(() => {
    if (selectedTask) 
    {
      setTitle(selectedTask.title);
      setDescription(selectedTask.description);
      setStatus(selectedTask.status);
      setPriority(selectedTask.priority);
      setDuedate(selectedTask.due_date);
      setAssignedTo(selectedTask.assigned_to || "");
      setFile(null)
    }
    else 
    {
      setTitle("");
      setDescription("");
      setStatus("pending");
      setPriority("low");
      setDuedate("");
      setAssignedTo("");
    }

    setErrors({});
  }, [selectedTask]);

  const handleSubmit = (e) => {
      e.preventDefault();

      const formData = new FormData();

      formData.append("title", title);
      formData.append("description", description);
      formData.append("status", status);
      formData.append("priority", priority);

      if (duedate) {
        formData.append("due_date", duedate);
      }

      if (assignedTo) {
        formData.append("assigned_to", Number(assignedTo));
      }

      if (file) {
        formData.append("attachment", file);
      }

      const url = selectedTask
        ? `https://task-app-project-6uvh.onrender.com/api/tasks/${selectedTask.id}/`
        : "https://task-app-project-6uvh.onrender.com/api/tasks/";

      const method = selectedTask ? axios.put : axios.post;

      method(url, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(() => {
          setErrors({});
          onSuccess();
        })

      
    .catch((err) => {

      let status = null;

      if (err.response && err.response.status) {
        status = err.response.status;
      }

      if (status === 401) {
        alert("Session expired. Please login again.");
      } 

      else if (status === 403) {
        alert("You are not allowed to perform this action.");
      } 

      else {
        if (err.response && err.response.data && err.response.data.errors) {
          setErrors(err.response.data.errors);
        } 
        else {
          setErrors({});
        }
      }
    });

  };

  return (
    <form onSubmit={handleSubmit}>

      <h3>{selectedTask ? "Edit Task" : "Create Task"}</h3>

      <input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)}/>
      {errors.title && <p className="error">{errors.title[0]}</p>}

      <textarea placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)}/>
      {errors.description && (<p className="error">{errors.description[0]}</p>)}

      <select value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="pending">Pending</option>
        <option value="in_progress">In Progress</option>
        <option value="completed">Completed</option>
      </select>

      <select value={priority} onChange={(e) => setPriority(e.target.value)}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>

      <input type="date" value={duedate || ""} onChange={(e) => setDuedate(e.target.value)}/>
      {errors.due_date && <p className="error">{errors.due_date[0]}</p>}

      <select value={assignedTo} onChange={(e) => setAssignedTo(e.target.value)}>
        <option value=""> Assign to user . . . </option>
        {users.map((user) => (
          <option key={user.id} value={user.id}>
            {user.username}
          </option>
        ))}
      </select>

      <input type="file" onChange={(e) => setFile(e.target.files[0])}/>

      <div className="form-actions">

        <button type="submit">
          {selectedTask ? "Update Task" : "Create Task"}
        </button>

        <button type="button" className="cancel-btn" onClick={onClose}>Close</button>

      </div>

    </form>
  );
}

export default TaskForm;
