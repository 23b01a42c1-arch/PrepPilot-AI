import { motion } from "framer-motion";
import heroRobot from "../../assets/images/hero-robot.png";
import Button from "../common/Button";

export default function Hero() {
  return (
    <section className="section min-h-screen pt-28 flex items-center">

      {/* LEFT */}

      <motion.div
        initial={{ x: -60, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="w-1/2"
      >

        <span className="inline-flex items-center px-5 py-2 rounded-full bg-cyan-500/10 border border-cyan-400/20 text-cyan-300 font-medium">

          AI Powered Interview Preparation Platform

        </span>

        <h1 className="mt-8 text-[80px] leading-[88px] font-extrabold">

          Ace Every

          <br />

          Interview with

          <br />

          <span className="gradientText">

            AI Intelligence

          </span>

        </h1>

        <h2 className="mt-8 text-3xl font-semibold">

          Your Personal AI Interview Coach

        </h2>

        <p className="mt-8 max-w-2xl text-slate-400 text-xl leading-9">

          Prepare for technical, HR and behavioral interviews using AI.
          Analyze your resume, receive personalized feedback,
          and monitor your progress through interactive reports.

        </p>

        <div className="mt-10 flex gap-5">

          <Button>

            Get Started

          </Button>

          <Button variant="secondary">

            Learn More

          </Button>

        </div>

      </motion.div>

      {/* RIGHT */}

      <motion.div
        animate={{ y: [0, -15, 0] }}
        transition={{
          duration: 4,
          repeat: Infinity,
        }}
        className="w-1/2 flex justify-end"
      >

        <img
          src={heroRobot}
          alt="PrepPilot AI"
          className="w-[760px] object-contain"
        />

      </motion.div>

    </section>
  );
}