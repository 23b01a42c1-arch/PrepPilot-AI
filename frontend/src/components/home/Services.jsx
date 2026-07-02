import { motion } from "framer-motion";
import {
  FaRobot,
  FaFileAlt,
  FaChartLine,
  FaHistory,
} from "react-icons/fa";

const services = [
  {
    icon: <FaRobot />,
    title: "AI Mock Interviews",
    description:
      "Practice HR, Technical and Behavioral interviews with intelligent AI.",
  },
  {
    icon: <FaFileAlt />,
    title: "Resume Analyzer",
    description:
      "Analyze your resume and receive ATS score with improvement suggestions.",
  },
  {
    icon: <FaChartLine />,
    title: "Performance Reports",
    description:
      "Track confidence, communication and interview performance visually.",
  },
  {
    icon: <FaHistory />,
    title: "Interview History",
    description:
      "Review all previous interviews and monitor your improvement over time.",
  },
];

export default function Services() {
  return (
    <section
      id="services"
      className="section py-32"
    >
      <div className="text-center">

        <span className="text-cyan-400 font-semibold">
          OUR SERVICES
        </span>

        <h2 className="text-5xl font-bold mt-4">
          Everything You Need
          <br />
          To Crack Your Interview
        </h2>

      </div>

      <div className="grid grid-cols-2 gap-8 mt-20">

        {services.map((service, index) => (

          <motion.div
            key={index}
            whileHover={{
              y: -8,
            }}
            transition={{
              duration: .3,
            }}
            className="glass rounded-3xl p-8 border border-cyan-500/10 hover:border-cyan-400/40"
          >

            <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 flex items-center justify-center text-3xl text-cyan-400">

              {service.icon}

            </div>

            <h3 className="text-2xl font-bold mt-6">

              {service.title}

            </h3>

            <p className="text-slate-400 leading-8 mt-4">

              {service.description}

            </p>

          </motion.div>

        ))}

      </div>

    </section>
  );
}