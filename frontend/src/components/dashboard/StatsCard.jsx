import { motion } from "framer-motion";

export default function StatsCard({
  title,
  value,
  icon,
}) {
  return (
    <motion.div
      whileHover={{
        y: -6,
        scale: 1.02,
      }}
      className="glass rounded-3xl border border-cyan-500/20 p-6"
    >
      <div className="flex items-center justify-between">

        <div>

          <p className="text-slate-400">
            {title}
          </p>

          <h2 className="mt-3 text-4xl font-bold">
            {value}
          </h2>

        </div>

        <div className="text-5xl text-cyan-400">
          {icon}
        </div>

      </div>
    </motion.div>
  );
}