import { useState, useContext } from "react";
import { AuthContext } from "./AuthContext";
import "./Login.css";

function Login() {

  const { loginUser } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState("");

  const validate = () => {
    let newErrors = {};

    if (!username.trim()) {
      newErrors.username = "Username is required";
    } 

    if (!password.trim()) {
      newErrors.password = "Password is required";
    } 
    else if (password.length <= 4) {
      newErrors.password = "Password must be greater than 4 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    
    e.preventDefault();

    setMessage("");
    setErrors({});

    if (!validate()) 
      return;

    try {
      const response = await fetch("http://127.0.0.1:8000/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(
        {
          username: username,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) 
      {
        localStorage.setItem("token", data.access);
        loginUser(data);
        setMessage("Login successful!");
      } 
      else {
        if (data.errors) {
          if (data.errors.detail) {
            setMessage(data.errors.detail);
          } 
          else {
            setErrors(data.errors);
          }
        } 
        else {
          setMessage("Login failed");
        }
      }
    } catch (error) {
      setMessage("Something went wrong");
    }
  };

  return (
    <div className="login-container">
      <form className="login-box" onSubmit={handleSubmit}>
        <h2 className="login-title">Login</h2>

        <input type="text" placeholder="Username" value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="login-input" />

        {errors.username && (
          <p className="error-text">{errors.username}</p>
        )}

        <input type="password" placeholder="Password" value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="login-input"/>
        
        {errors.password && (
          <p className="error-text">{errors.password}</p>
        )}

        <button type="submit" className="login-btn">Login</button>

        {message && <p className="login-message">{message}</p>}
        
      </form>
    </div>
  );
}

export default Login;
