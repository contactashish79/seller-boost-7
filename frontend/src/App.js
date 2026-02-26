import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "@/App.css";
import LandingPage from "./pages/LandingPage";
import Dashboard from "./pages/Dashboard";
import Editor from "./pages/Editor";
import { Toaster } from "./components/ui/sonner";

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  const PrivateRoute = ({ children }) => {
    return token ? children : <Navigate to="/" />;
  };

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage setToken={setToken} isAuthenticated={!!token} />} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/editor/:projectId?" element={<PrivateRoute><Editor /></PrivateRoute>} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" />
    </div>
  );
}

export default App;