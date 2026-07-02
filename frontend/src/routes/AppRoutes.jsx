import { Routes, Route } from "react-router-dom";

import ProtectedRoute from "../components/auth/ProtectedRoute";

import Home from "../pages/Home/Home";
import Login from "../pages/Login/Login";
import Register from "../pages/Register/Register";
import Dashboard from "../pages/Dashboard/Dashboard";
import InterviewSetup from "../pages/Interview/InterviewSetup";
import InterviewSession from "../pages/Interview/InterviewSession";

export default function AppRoutes() {
  return (
    <Routes>

      <Route path="/" element={<Home />} />

      <Route path="/login" element={<Login />} />

      <Route path="/register" element={<Register />} />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/interview"
        element={
          <ProtectedRoute>
            <InterviewSetup />
          </ProtectedRoute>
        }
      />

      <Route
        path="/interview/session"
        element={
          <ProtectedRoute>
            <InterviewSession />
          </ProtectedRoute>
        }
      />

    </Routes>
  );
}