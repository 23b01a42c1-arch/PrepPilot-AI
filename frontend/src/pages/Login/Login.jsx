import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  FaEnvelope,
  FaLock,
  FaEye,
  FaEyeSlash,
  FaRobot,
} from "react-icons/fa";

import Input from "../../components/common/Input";
import Button from "../../components/common/Button";
import api from "../../api/axios";

export default function Login() {

  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.email || !form.password) {
      alert("Please fill all fields.");
      return;
    }

    try {

      const response = await api.post("/auth/login", form);

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      alert("Login Successful!");

      navigate("/dashboard");

    } catch (error) {

      alert(
        error.response?.data?.detail ||
        "Login Failed"
      );

    }
  };

  return (

    <div className="relative flex min-h-screen items-center justify-center bg-[#020817] px-6">

      <div className="absolute left-1/2 top-1/2 h-[700px] w-[700px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-cyan-500/10 blur-[140px]" />

      <div className="glass glow relative z-10 w-full max-w-[520px] rounded-[32px] border border-cyan-500/20 p-8">

        <div className="text-center">

          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border border-cyan-500/20 bg-cyan-500/10">

            <FaRobot className="text-2xl text-cyan-400"/>

          </div>

          <h1 className="text-3xl font-bold">

            PrepPilot
            <span className="text-cyan-400">AI</span>

          </h1>

          <p className="mt-2 text-slate-400">

            Your Personal AI Interview Coach

          </p>

        </div>

        <div className="mt-8">

          <h2 className="text-3xl font-bold">

            Welcome Back

          </h2>

          <p className="mt-2 text-slate-400">

            Login to continue your interview journey.

          </p>

        </div>

        <form
          onSubmit={handleSubmit}
          className="mt-6 space-y-5"
        >

          <Input
            label="Email"
            name="email"
            value={form.email}
            onChange={handleChange}
            placeholder="Enter your email"
            icon={<FaEnvelope />}
          />

          <div className="relative">

            <Input
              label="Password"
              name="password"
              value={form.password}
              onChange={handleChange}
              type={showPassword ? "text" : "password"}
              placeholder="Enter your password"
              icon={<FaLock />}
            />

            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-5 top-[46px] text-slate-400 hover:text-cyan-400"
            >
              {showPassword ? <FaEyeSlash/> : <FaEye/>}
            </button>

          </div>

          <div className="text-right">

            <Link
              to="/forgot-password"
              className="text-cyan-400 hover:underline"
            >
              Forgot Password?
            </Link>

          </div>

          <Button
            type="submit"
            className="w-full"
          >
            Login
          </Button>

          <p className="text-center text-slate-400">

            Don't have an account?{" "}

            <Link
              to="/register"
              className="font-semibold text-cyan-400 hover:underline"
            >
              Sign Up
            </Link>

          </p>

        </form>

      </div>

    </div>

  );
}