import { useState, useEffect } from "react";
import axios from "axios";
import TaskForm from "./TaskForm";
import { useSearchParams } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
// import ErrorBoundary from "./ErrorBoundary";
import "./TaskList.css";

function TaskList() {
  
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState();

  const [selectedTask, setSelectedTask] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [totalPages,setTotalPages] = useState(1);
  const [temp, setTemp] = useState("");
  const [totalCount, setTotalCount] = useState(0);
  const [role, setRole] = useState("");

  const [searchParams, setSearchParams] = useSearchParams();
  const page = searchParams.get("page") || 1;
  const search = searchParams.get("search") || "";
  const pageSize = Number(searchParams.get("page_size")) || 6;

  const status = searchParams.get("status") || "";
  const priority = searchParams.get("priority") || "";
  const createdAfter = searchParams.get("created_at_after") || "";
  const createdBefore = searchParams.get("created_at_before") || "";

  const [socket, setSocket] = useState(null); // eslint-disable-next-line react-hooks/exhaustive-deps

  const token = localStorage.getItem("token");


  const fetchTasks = () => {
    setLoading(true);
    axios
      .get("https://task-app-project-6uvh.onrender.com/api/tasks/", 
      {
        headers: { Authorization: `Bearer ${token}` },

      params: {
        page,
        search,
        page_size: pageSize,
        status,
        priority,
        created_at_after: createdAfter,
        created_at_before: createdBefore,
      },

      })
      
      .then((res) => {
        setTasks(res.data.results);
        setTotalCount(res.data.count);
        setTotalPages(Math.ceil(res.data.count / pageSize));
      })
      
      .catch(() => setError("Failed to load tasks"))
      .finally(() => setLoading(false));
  };

    // eslint-disable-next-line react-hooks/exhaustive-deps

      useEffect(() => {
        fetchTasks();
      },[searchParams]);

    //   useEffect(() => {
    //   throw new Error("Test error in TaskList!");
    // }, []);


    // eslint-disable-next-line react-hooks/exhaustive-deps

      useEffect(() => {
     
      const ws = new WebSocket("ws://127.0.0.1:8000/ws/tasks/");

      ws.onopen = () => {
        console.log("WebSocket connected");
      };

      ws.onmessage = (event) => {

        const data = JSON.parse(event.data);
        console.log("WebSocket message received:", data);

        if (data.action === "created") {
          setTasks((prev) => [data.task, ...prev]);
          toast.success(`Task Created: ${data.task.title}`);
        }

        if (data.action === "updated") {
          setTasks((prev) => prev.map((task) =>
              task.id === data.task.id ? data.task : task )
          );
          toast.info(`Task Updated: ${data.task.title}`);
        }

        if (data.action === "deleted") {
          setTasks((prev) =>
            prev.filter((task) => task.id !== data.task.id)
          );
          toast.error(`Task Deleted: ID ${data.task.id}`);
        }
      };

      ws.onclose = () => {
        console.log("WebSocket disconnected");
      };

      setSocket(ws);

      return () => ws.close();
    }, []);


    // eslint-disable-next-line react-hooks/exhaustive-deps
      
      useEffect(() => {

      axios.get("https://task-app-project-6uvh.onrender.com/api/user-groups/", 
      {
        headers: { Authorization: `Bearer ${token}` },
      })

      .then(res => 
      {
        setRole(res.data.groups[0]);
      })

      .catch(err => console.log(err));
      }, []);


      const deleteTask = (id) => {
        if (!window.confirm("Delete this task?")) return;

        axios
          .delete(`https://task-app-project-6uvh.onrender.com/api/tasks/${id}/`, 
          {
            headers: { Authorization: `Bearer ${token}` },
          })

          .then(() => fetchTasks())
          .catch((err) => {
            if (err.response?.status === 403) {
              alert("You are not allowed to delete this task");
            } 
            else {
              alert("Delete failed");
            }
          });
      };
      
      const exportPDF = () => {

        axios.get(
          "https://task-app-project-6uvh.onrender.com/api/export/tasks/pdf/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
            responseType: "blob",
          }
        )
        .then((res) => {

          const file = new Blob([res.data], { type: "application/pdf" });
          const url = window.URL.createObjectURL(file);

          const link = document.createElement("a");
          link.href = url;

          link.download = "tasks.pdf";
          link.click();

        })

        .catch(() => {
          alert("PDF export failed");
        });
      };

      const openCreateForm = () => {
        setSelectedTask(null);
        setShowForm(true);
      };


      const openEditForm = (task) => {
        setSelectedTask(task);
        setShowForm(true);
      };


      const handleFormSuccess = () => {
        setShowForm(false);
        setSelectedTask(null);
        fetchTasks();
      };


    if (loading) 
      return <p>Loading tasks...</p>;
    if (error) 
      return <p>{error}</p>;

  return (
    
    <div className="task-container">

      <ToastContainer position="top-right" autoClose={3000} />

      <input type="text" placeholder="Search tasks..." value={temp}
        onChange={(e) => setTemp(e.target.value)}
        className="search-input"/>

      <button className="search-btn"
        onClick={() => {
            const params = new URLSearchParams(searchParams);
            params.set("search", temp);
            params.set("page", 1);
            setSearchParams(params);
        }}> Search</button>

        <select value={pageSize}
          onChange={(e) => {
            const params = new URLSearchParams(searchParams);
            params.set("page_size", e.target.value);
            params.set("page", 1);
            setSearchParams(params);
          }}className="page-size-dropdown">
            

      {(() => {

        let options = [];

        for (let i = 6; i <= totalCount; i += 6) {
          options.push(
            <option key={i} value={i}>{i}</option>
          );
        }

        return options;
        
      })()}

      <option value={totalCount}>All</option>

    </select>

    
    <div className="filter-bar">

      <select className="filter-item" value={status} onChange={(e) => {

          const params = new URLSearchParams(searchParams);
         
          if (e.target.value) 
          {
            params.set("status", e.target.value);
          } 
          else 
          {
            params.delete("status");
          }

          params.set("page", 1);
          setSearchParams(params);
        }} >

        <option value="">All Status</option>
        <option value="pending">Pending</option>
        <option value="completed">Completed</option>

      </select>

      <select className="filter-item" value={priority} onChange={(e) => {

          const params = new URLSearchParams(searchParams);
          if (e.target.value) 
          {
            params.set("priority", e.target.value);
          } 
          else 
          {
            params.delete("priority");
          }

          params.set("page", 1);
          setSearchParams(params);
        }} >

        <option value="">All Priority</option>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>

      </select>


      <div className="date-filter">

      <input type="date" value={createdAfter ? createdAfter.split("T")[0] : ""}
      
      onChange={(e) => {

        const params = new URLSearchParams(searchParams);

        if (e.target.value) {
          params.set("created_at_after", `${e.target.value}T00:00:00`);
        }
        else 
        {
          params.delete("created_at_after");
        }

        params.set("page", 1);
        setSearchParams(params);

      }} /> 
      
        
      <input type="date" value={createdBefore ? createdBefore.split("T")[0] : ""}
       onChange={(e) => {
       
        const params = new URLSearchParams(searchParams);
       
        if (e.target.value) {
          params.set("created_at_before", `${e.target.value}T23:59:59`);
        } 
        else {
          params.delete("created_at_before");
        }

        params.set("page", 1);
        setSearchParams(params);

      }} />

      </div>

    </div>

      {(role === "Admin" || role === "Manager") && (
      <button className="create-btn" onClick={openCreateForm}>Add Task</button>
      )}

      <button className="export-btn" onClick={exportPDF}>Export PDF</button>

      {showForm && (
        
        <div className="modal-overlay">

          <div className="modal-content">
            
          <TaskForm
              selectedTask={selectedTask}
              onSuccess={handleFormSuccess}
              onClose={() => setShowForm(false)}
            />
          </div>

        </div>
      )}

      <h2>Task List</h2>

      {tasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        <>
        <ul>
          {tasks.map((task) => (

            <li key={task.id}>
              <p><b>{task.title}</b></p>
              <i>{task.description}</i>
              <p>Status: {task.status}</p>
              <p>Priority: {task.priority}</p>
              <p>Created At: {new Date(task.created_at).toLocaleString()}</p>
              <p>Due: {task.due_date}</p>

              {task.attachment && (

                <div className="attachment">
                  {task.attachment.endsWith(".jpg") ||task.attachment.endsWith(".jpeg") ||
                  task.attachment.endsWith(".png") 
                  ? 
                  (
                    <img src={task.attachment} alt="task file" className="task-image"/>
                  ) 
                  : 
                  (
                    <a href={task.attachment} target="_blank" rel="noreferrer" className="file-link">
                      Download File
                    </a>
                  )}
                  
                </div>
              )}

              {(role === "Admin" || role === "Manager") && (
                <button onClick={() => openEditForm(task)}>Edit</button>
              )}

              {role === "Admin" && (
                <button onClick={() => deleteTask(task.id)}>Delete</button>
              )}
              
            </li>

          ))}
        </ul>

      <div className="pagination">
       
        <button disabled={page === 1}
            onClick={() => {
            const params = new URLSearchParams(searchParams);
            params.set("page", page - 1);
            setSearchParams(params);
        }}>Prev</button>

        {(() => {
        
        let buttons = [];

        for (let i = 1; i <= totalPages; i++) {
          buttons.push(
            <button
              key={i}
              onClick={() => {
                const params = new URLSearchParams(searchParams);
                params.set("page", i);
                setSearchParams(params);
              }} >{i}</button>
          );
        }
        return buttons;

      })()}

        <span> Page {page} of {totalPages} </span>

        <button  disabled={page === totalPages}
          onClick={() => {
            const params = new URLSearchParams(searchParams);
            params.set("page", page + 1);
            setSearchParams(params);
        }}> Next</button>

      </div>

      </>

      )}

    </div>
    
  );
}

export default TaskList;
