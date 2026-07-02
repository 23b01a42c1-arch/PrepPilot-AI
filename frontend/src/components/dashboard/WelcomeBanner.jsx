import { motion } from "framer-motion";

export default function WelcomeBanner({ user }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="glass rounded-3xl border border-cyan-500/20 p-8"
    >
      <h1 className="text-4xl font-bold">
        Welcome Back 
      </h1>

      <h2 className="mt-3 text-2xl font-semibold text-cyan-400">
        {user?.full_name}
      </h2>

      <p className="mt-4 text-slate-400">
        Ready to ace your next interview? Start practicing and improve your confidence with AI-powered feedback.
      </p>
    </motion.div>
  );
}