import { motion } from "framer-motion";

const steps = [
  {
    number: "01",
    title: "Create an Account",
    description:
      "Register and create your PrepPilot AI profile.",
  },
  {
    number: "02",
    title: "Upload Your Resume",
    description:
      "Get ATS analysis and personalized recommendations.",
  },
  {
    number: "03",
    title: "Practice Interviews",
    description:
      "Take AI-powered mock interviews with voice interaction.",
  },
  {
    number: "04",
    title: "Track Your Progress",
    description:
      "View reports and improve with every interview.",
  },
];

export default function HowItWorks() {
  return (
    <section
      id="how"
      className="section py-32"
    >
      <div className="text-center">

        <span className="text-cyan-400 font-semibold">
          HOW IT WORKS
        </span>

        <h2 className="text-5xl font-bold mt-4">

          Four Simple Steps

        </h2>

      </div>

      <div className="grid grid-cols-4 gap-8 mt-20">

        {steps.map((step) => (

          <motion.div
            whileHover={{
              y: -8,
            }}
            key={step.number}
            className="glass rounded-3xl p-8 text-center"
          >

            <div className="w-16 h-16 rounded-full bg-cyan-400 text-slate-900 flex items-center justify-center font-bold text-2xl mx-auto">

              {step.number}

            </div>

            <h3 className="mt-8 text-2xl font-bold">

              {step.title}

            </h3>

            <p className="text-slate-400 mt-5 leading-8">

              {step.description}

            </p>

          </motion.div>

        ))}

      </div>

    </section>
  );
}