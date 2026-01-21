import { useContext } from "react";
import { AuthContext } from "./AuthContext";
import "./Header.css";
import UserAvatar from "./UserAvatar"; 

function Header() {

  const { user, logoutUser } = useContext(AuthContext);

  return (
    <header className="header">

      <h1 className="logo">Task Manager</h1>

      <div className="user-info">

        {user ? (
          <>
            <span>Hello, {user.username}</span>
            <UserAvatar />
            <button onClick={logoutUser}>Logout</button>
          </>
        ) : (
          "Guest"
        )}

      </div>

    </header>
  );

}

export default Header;
