import { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

function AuthProvider({ children }) {

  const [user, setUser] = useState(null);
  const [tokens, setTokens] = useState(null);
  const [loading, setLoading] = useState(true);

  // eslint-disable-next-line react-hooks/exhaustive-deps

  useEffect(() => 
  {
    const storedTokens = localStorage.getItem("tokens");

    if (storedTokens) {
      const parsedTokens = JSON.parse(storedTokens);
      setTokens(parsedTokens);
      fetchProfile(parsedTokens.access);
    } 
    else {
      setLoading(false);
    }

  }, []);

  const fetchProfile = async (accessToken) => {
    try {
      const response = await fetch("https://task-app-project-6uvh.onrender.com/api/profile/", {
        headers: 
        {
          Authorization: "Bearer " + accessToken,
        },
      });

      if (response.ok) 
      {
        const userData = await response.json();
        setUser(userData);
      } 
      
      else {
        logoutUser();
      }

    }
     catch {
      logoutUser();
    }
     finally {
      setLoading(false);
    }
  };

  const loginUser = async (tokenData) => {
    setTokens(tokenData);
    localStorage.setItem("tokens", JSON.stringify(tokenData));
    fetchProfile(tokenData.access);
  };

  const logoutUser = () => {
    setUser(null);
    setTokens(null);
    localStorage.clear();
  };

  return (
    <AuthContext.Provider value={{ user, tokens, loginUser, logoutUser, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
