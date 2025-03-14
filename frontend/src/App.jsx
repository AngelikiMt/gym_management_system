import React from "react";
import {BrowserRouter, Routes, Route, Navigation, Navigate} from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";

function Logout() {
  localStorage.clear();
  return <Navigate to="/users/login" />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path="/users/login" element={<Login />} />
        <Route path="/users/register" element={<Register />} />
        <Route path="/users/logout" element={<Logout />} />
        <Route path="*" element={<NotFound />} ></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
