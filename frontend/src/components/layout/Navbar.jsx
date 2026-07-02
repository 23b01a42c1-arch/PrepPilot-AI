import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import Button from "../common/Button";
import { FaRobot } from "react-icons/fa";

export default function Navbar() {
  return (
    <motion.nav
      initial={{ y: -70, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.7 }}
      className="fixed top-0 left-0 w-full z-50 backdrop-blur-xl bg-slate-950/60 border-b border-cyan-500/10"
    >
      <div className="max-w-7xl mx-auto px-8 h-20 flex items-center justify-between">

        <Link
          to="/"
          className="flex items-center gap-3"
        >
          <div className="w-12 h-12 rounded-2xl bg-cyan-400 flex items-center justify-center shadow-[0_0_30px_rgba(34,211,238,.5)]">

            <FaRobot className="text-slate-900 text-xl"/>

          </div>

          <div>

            <h1 className="text-2xl font-bold">

              PrepPilot

              <span className="text-cyan-400">
                AI
              </span>

            </h1>

            <p className="text-xs text-slate-400">
              Your Personal AI Interview Coach
            </p>

          </div>

        </Link>

        <div className="hidden lg:flex gap-10 text-slate-300">

          <a href="#services">Services</a>

          <a href="#how">How It Works</a>

          <a href="#about">About</a>

        </div>

        <div className="flex gap-4">

          <Link to="/login">

            <Button variant="secondary">
              Login
            </Button>

          </Link>

          <Link to="/register">

            <Button>
              Sign Up
            </Button>

          </Link>

        </div>

      </div>
    </motion.nav>
  );
}