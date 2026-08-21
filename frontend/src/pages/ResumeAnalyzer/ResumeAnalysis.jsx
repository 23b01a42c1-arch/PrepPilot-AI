import { useLocation, useNavigate } from "react-router-dom";
import {
  FaArrowRight,
  FaCheckCircle,
  FaChartPie,
  FaClipboardCheck,
  FaRocket,
  FaSearch,
} from "react-icons/fa";



export default function ResumeAnalysis() {
  const navigate = useNavigate();
  const { state } = useLocation();
  console.log("========== RESUME ANALYSIS STATE ==========");
  console.log(state);
  console.log("match_percentage:", state?.match_percentage);
  console.log("ats_score:", state?.ats_score);
  console.log("readiness_score:", state?.readiness_score);
  console.log("match_breakdown:", state?.match_breakdown);
  console.log("==========================================");

  if (!state) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#020817] text-white">
        No analysis found.
      </div>
    );
  }

  const {
    match_percentage,
    ats_score,
    readiness_score,
    matched_skills,
    missing_skills,
    strengths,
    weaknesses,
    suggestions,
    match_breakdown,
    resume_data,
    jd_data,
  } = state;

  const Circle = ({ value, title, color }) => (
    <div className="rounded-3xl border border-cyan-500/20 bg-[#0F172A] p-8 shadow-xl">
      <div
        className={`mx-auto flex h-36 w-36 items-center justify-center rounded-full border-8 ${color}`}
      >
        <span className="text-4xl font-bold text-white">
          {value}%
        </span>
      </div>

      <h2 className="mt-6 text-center text-xl font-semibold text-white">
        {title}
      </h2>
    </div>
  );

  return (
    <div className="min-h-screen bg-[#020817] px-8 py-10">

      {/* Header */}

      <div className="mb-10 flex items-center justify-between">

        <div>

          <h1 className="text-5xl font-bold text-white">

            Resume Analysis

          </h1>

          <p className="mt-3 text-slate-400">

            AI powered resume screening and interview readiness.

          </p>

        </div>

        <button
          onClick={() =>
            navigate("/interview", {
              state: {
                resume_data,
                jd_data,
              },
            })
          }
          className="flex items-center gap-3 rounded-2xl bg-cyan-400 px-8 py-4 font-bold text-black transition hover:scale-105"
        >
          Start AI Interview
          <FaArrowRight />
        </button>

      </div>

      {/* Score Cards */}

      <div className="grid gap-8 lg:grid-cols-3">

        <Circle
          value={match_percentage}
          title="Resume Match"
          color="border-green-500"
        />

        <Circle
          value={ats_score}
          title="ATS Score"
          color="border-orange-500"
        />

        <Circle
          value={readiness_score}
          title="Interview Readiness"
          color="border-cyan-400"
        />

      </div>

      {/* Match Breakdown */}

      <div className="mt-10 rounded-3xl border border-cyan-500/20 bg-[#0F172A] p-8">

        <div className="mb-8 flex items-center gap-3">

          <FaChartPie className="text-3xl text-cyan-400" />

          <h2 className="text-3xl font-bold text-white">

            Match Breakdown

          </h2>

        </div>
                <div className="space-y-8">

          {/* Skills */}

          <div>

            <div className="mb-2 flex justify-between text-white">

              <span>Skills Match</span>

              <span>{match_breakdown?.skills || 0}%</span>

            </div>

            <div className="h-3 rounded-full bg-slate-700">

              <div
                className="h-3 rounded-full bg-cyan-400"
                style={{
                  width: `${match_breakdown?.skills || 0}%`,
                }}
              />

            </div>

          </div>

          {/* Projects */}

          <div>

            <div className="mb-2 flex justify-between text-white">

              <span>Projects Match</span>

              <span>{match_breakdown?.projects || 0}%</span>

            </div>

            <div className="h-3 rounded-full bg-slate-700">

              <div
                className="h-3 rounded-full bg-green-400"
                style={{
                  width: `${match_breakdown?.projects || 0}%`,
                }}
              />

            </div>

          </div>

          {/* Experience */}

          <div>

            <div className="mb-2 flex justify-between text-white">

              <span>Experience Match</span>

              <span>{match_breakdown?.experience || 0}%</span>

            </div>

            <div className="h-3 rounded-full bg-slate-700">

              <div
                className="h-3 rounded-full bg-orange-400"
                style={{
                  width: `${match_breakdown?.experience || 0}%`,
                }}
              />

            </div>

          </div>

          {/* Education */}

          <div>

            <div className="mb-2 flex justify-between text-white">

              <span>Education Match</span>

              <span>{match_breakdown?.education || 0}%</span>

            </div>

            <div className="h-3 rounded-full bg-slate-700">

              <div
                className="h-3 rounded-full bg-pink-400"
                style={{
                  width: `${match_breakdown?.education || 0}%`,
                }}
              />

            </div>

          </div>

        </div>

      </div>

      {/* Skills Section */}

      <div className="mt-10 grid gap-8 lg:grid-cols-2">

        {/* Matching Skills */}

        <div className="rounded-3xl border border-green-500/20 bg-[#0F172A] p-8">

          <div className="mb-6 flex items-center gap-3">

            <FaCheckCircle className="text-3xl text-green-400" />

            <h2 className="text-2xl font-bold text-white">

              Matching Skills

            </h2>

          </div>

          <div className="flex flex-wrap gap-3">

            {matched_skills?.map((skill, index) => (

              <span
                key={index}
                className="rounded-full bg-green-500/20 px-5 py-3 text-green-300"
              >

                {skill}

              </span>

            ))}

          </div>

        </div>

        {/* Missing Skills */}

        <div className="rounded-3xl border border-red-500/20 bg-[#0F172A] p-8">

          <div className="mb-6 flex items-center gap-3">

            <FaSearch className="text-3xl text-red-400" />

            <h2 className="text-2xl font-bold text-white">

              Missing Skills

            </h2>

          </div>

          <div className="flex flex-wrap gap-3">

            {missing_skills?.map((skill, index) => (

              <span
                key={index}
                className="rounded-full bg-red-500/20 px-5 py-3 text-red-300"
              >

                {skill}

              </span>

            ))}

          </div>

        </div>

      </div>
            {/* Strengths & Weaknesses */}

      <div className="mt-10 grid gap-8 lg:grid-cols-2">

        {/* Strengths */}

        <div className="rounded-3xl border border-green-500/20 bg-[#0F172A] p-8">

          <div className="mb-6 flex items-center gap-3">

            <FaClipboardCheck className="text-3xl text-green-400" />

            <h2 className="text-2xl font-bold text-white">

              Resume Strengths

            </h2>

          </div>

          <div className="space-y-4">

            {strengths?.map((item, index) => (

              <div
                key={index}
                className="rounded-2xl bg-green-500/10 p-4 text-green-300"
              >

                ✓ {item}

              </div>

            ))}

          </div>

        </div>

        {/* Weaknesses */}

        <div className="rounded-3xl border border-red-500/20 bg-[#0F172A] p-8">

          <div className="mb-6 flex items-center gap-3">

            <FaSearch className="text-3xl text-red-400" />

            <h2 className="text-2xl font-bold text-white">

              Areas to Improve

            </h2>

          </div>

          <div className="space-y-4">

            {weaknesses?.map((item, index) => (

              <div
                key={index}
                className="rounded-2xl bg-red-500/10 p-4 text-red-300"
              >

                • {item}

              </div>

            ))}

          </div>

        </div>

      </div>

      {/* AI Suggestions */}

      <div className="mt-10 rounded-3xl border border-orange-500/20 bg-[#0F172A] p-8">

        <div className="mb-6 flex items-center gap-3">

          <FaRocket className="text-3xl text-orange-400" />

          <h2 className="text-2xl font-bold text-white">

            AI Suggestions

          </h2>

        </div>

        <div className="space-y-4">

          {suggestions?.map((item, index) => (

            <div
              key={index}
              className="rounded-2xl bg-orange-500/10 p-5 text-orange-200"
            >

              {item}

            </div>

          ))}

        </div>

      </div>

      {/* Ready Card */}

      <div className="mt-10 rounded-3xl border border-cyan-500/20 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 p-10">

        <div className="flex flex-col items-center text-center">

          <h2 className="text-4xl font-bold text-white">

            Ready to Start Your AI Interview?

          </h2>

          <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-300">

            Your resume has been analyzed successfully.

            PrepPilot AI will generate personalized interview
            questions based on your resume, projects,
            technical skills and the uploaded Job Description.

          </p>

          <button

            onClick={() =>
              navigate("/interview", {
                state: {
                  resume_data,
                  jd_data
                }
              })
            }

            className="mt-8 flex items-center gap-3 rounded-2xl bg-cyan-400 px-10 py-5 text-xl font-bold text-black transition duration-300 hover:scale-105"

          >

            Start AI Interview

            <FaArrowRight />

          </button>

        </div>

      </div>

    </div>

  );

}