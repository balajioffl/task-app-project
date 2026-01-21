import AuthProvider, { AuthContext } from "./AuthContext";
import Login from "./Login";
import Header from "./Header";
import TaskList from "./TaskList";
import ErrorBoundary from "./ErrorBoundary";
import { useContext } from "react";
import { BrowserRouter } from "react-router-dom";


function AppContent() {
  const { user } = useContext(AuthContext);

  return (
    <div>
      {user ? (
        <>
          <Header />
          <ErrorBoundary>
            <TaskList />
          </ErrorBoundary>
        </>
      ) : (
        <Login />
      )}
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;