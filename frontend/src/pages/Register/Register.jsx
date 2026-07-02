import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  FaUser,
  FaEnvelope,
  FaLock,
  FaEye,
  FaEyeSlash,
  FaRobot,
} from "react-icons/fa";

import Input from "../../components/common/Input";
import Button from "../../components/common/Button";
import api from "../../api/axios";

export default function Register() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (
      !form.full_name ||
      !form.email ||
      !form.password ||
      !form.confirmPassword
    ) {
      alert("Please fill all fields.");
      return;
    }

    if (form.password !== form.confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    try {
      const response = await api.post("/auth/register", {
        full_name: form.full_name,
        email: form.email,
        password: form.password,
      });

      alert(response.data.message);

      navigate("/login");

    } catch (error) {
      alert(
        error.response?.data?.detail ||
        "Registration Failed"
      );
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[#020817] px-6">

      {/* Background Glow */}

      <div className="absolute left-1/2 top-1/2 h-[700px] w-[700px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-cyan-500/10 blur-[140px]" />

      <div className="relative z-10 glass glow w-full max-w-[520px] rounded-[32px] border border-cyan-500/20 p-8">

        {/* Logo */}

        <div className="text-center">

          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border border-cyan-500/20 bg-cyan-500/10">

            <FaRobot className="text-2xl text-cyan-400" />

          </div>

          <h1 className="text-3xl font-bold">

            PrepPilot
            <span className="text-cyan-400">AI</span>

          </h1>

          <p className="mt-2 text-slate-400">

            Your Personal AI Interview Coach

          </p>

        </div>

        {/* Heading */}

        <div className="mt-8">

          <h2 className="text-3xl font-bold">

            Create Account

          </h2>

          <p className="mt-2 text-slate-400">

            Join us and start your AI interview journey.

          </p>

        </div>

        {/* Form */}

        <form
          onSubmit={handleSubmit}
          className="mt-6 space-y-5"
        >

          <Input
            label="Full Name"
            name="full_name"
            value={form.full_name}
            onChange={handleChange}
            placeholder="Enter your full name"
            icon={<FaUser />}
          />

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
              placeholder="Create your password"
              icon={<FaLock />}
            />

            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-5 top-[46px] text-slate-400 hover:text-cyan-400"
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </button>

          </div>

          <div className="relative">

            <Input
              label="Confirm Password"
              name="confirmPassword"
              value={form.confirmPassword}
              onChange={handleChange}
              type={showConfirm ? "text" : "password"}
              placeholder="Confirm your password"
              icon={<FaLock />}
            />

            <button
              type="button"
              onClick={() => setShowConfirm(!showConfirm)}
              className="absolute right-5 top-[46px] text-slate-400 hover:text-cyan-400"
            >
              {showConfirm ? <FaEyeSlash /> : <FaEye />}
            </button>

          </div>

          <Button
            type="submit"
            className="w-full rounded-2xl bg-gradient-to-r from-cyan-500 to-sky-500 py-4 font-semibold text-black transition duration-300 hover:scale-[1.02] hover:shadow-[0_0_25px_rgba(34,211,238,.45)]"
          >

            Create Account

          </Button>

          <div className="relative py-3">

            <div className="border-t border-slate-700"></div>

            <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-[#0F172A] px-4 text-sm text-slate-500">

              OR

            </span>

          </div>

          <button
            type="button"
            className="glass flex h-14 w-full items-center justify-center gap-3 rounded-2xl border border-cyan-500/20 transition hover:border-cyan-400 hover:bg-cyan-500/5"
          >

            <img
              src="https://www.svgrepo.com/show/475656/google-color.svg"
              alt="Google"
              className="h-5 w-5"
            />

            Continue with Google

          </button>

          <p className="text-center text-slate-400">

            Already have an account?{" "}

            <Link
              to="/login"
              className="font-semibold text-cyan-400 hover:underline"
            >
              Login
            </Link>

          </p>

        </form>

      </div>

    </div>
  );
}