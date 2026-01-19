// src/App.js
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import MainPanel from "./components/MainPanel/MainPanel";
import TestModelPage from "./components/TestModelPage/TestModelPage";
import Sidebar from "./components/Sidebar/Sidebar";

import "./App.css";
import { API_URL } from "./config";
import axios from "axios";

// 🔧 Настройка axios (можно вынести в отдельный файл позже)
axios.defaults.baseURL = API_URL;

// Добавим интерцептор для логирования ошибок (опционально)
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("Axios error:", error);
    return Promise.reject(error);
  }
);

function AppContent() {
  return (
    <div className="app-container">
      <main className="content">
      <Sidebar/>
        <Routes>
          <Route path="/" element={<Navigate to="/description" replace />} />
          <Route path="/description" element={<MainPanel />} />
          <Route path="/test-model" element={<TestModelPage />} />
        </Routes>
      </main>
    </div>
  );
}


function App() {
  return (
    <Router>
      <div className="body">
        <AppContent />
      </div>
    </Router>
  );
}

export default App;
