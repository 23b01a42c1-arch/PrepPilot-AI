import { useLocation, useNavigate } from "react-router-dom";
import {
  FaChartBar,
  FaArrowLeft,
  FaMicrophone,
  FaCheckCircle,
  FaBrain,
  FaComments,
  FaBullseye,
} from "react-icons/fa";

export default function InterviewReport() {

  const navigate = useNavigate();

  const { state } = useLocation();

  // -----------------------------
  // Empty State
  // -----------------------------

  if (!state) {

    return (

      <div className="flex min-h-screen items-center justify-center bg-[#020817] px-6">

        <div className="w-full max-w-3xl rounded-3xl border border-cyan-500/20 bg-[#08111f] p-12 text-center">

          <div className="mx-auto flex h-24 w-24 items-center justify-center rounded-full bg-cyan-500/10">

            <FaChartBar className="text-5xl text-cyan-400" />

          </div>

          <h1 className="mt-8 text-4xl font-bold text-white">

            No Interview Report Yet

          </h1>

          <p className="mt-6 text-lg text-slate-400 leading-8">

            Complete an AI Interview to unlock your
            personalized interview report.

          </p>

          <button

            onClick={() => navigate("/interview")}

            className="mt-10 rounded-2xl bg-cyan-400 px-8 py-4 font-bold text-black transition hover:scale-105"

          >

            <FaMicrophone className="mr-3 inline" />

            Start AI Interview

          </button>

        </div>

      </div>

    );

  }

  // -----------------------------
  // Report Data
  // -----------------------------

  const {

    overall_score,

    technical_score,

    communication_score,

    topic_scores,

    strengths,

    weaknesses,

    recommendation,

    learning_roadmap,

  } = state;

  return (

    <div className="min-h-screen bg-[#020817] text-white">

      {/* Header */}

      <div className="border-b border-cyan-500/20 bg-[#08111f]">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-10 py-8">

          <div>

            <h1 className="text-4xl font-bold">

              Interview Report

            </h1>

            <p className="mt-3 text-slate-400">

              AI-generated performance analysis

            </p>

          </div>

          <button

            onClick={() => navigate("/dashboard")}

            className="rounded-xl border border-cyan-500/20 px-6 py-3 transition hover:bg-cyan-500/10"

          >

            <FaArrowLeft className="mr-2 inline" />

            Dashboard

          </button>

        </div>

      </div>

      <div className="mx-auto max-w-7xl px-10 py-10">

        {/* Score Cards */}

        <div className="grid gap-6 md:grid-cols-3">

          <div className="rounded-3xl border border-cyan-500/20 bg-[#08111f] p-8">

            <div className="flex items-center gap-4">

              <div className="rounded-full bg-cyan-500/10 p-4">

                <FaBullseye className="text-3xl text-cyan-400" />

              </div>

              <div>

                <p className="text-slate-400">

                  Overall Score

                </p>

                <h2 className="text-5xl font-bold text-cyan-400">

                  {overall_score}%

                </h2>

              </div>

            </div>

          </div>

          <div className="rounded-3xl border border-cyan-500/20 bg-[#08111f] p-8">

            <div className="flex items-center gap-4">

              <div className="rounded-full bg-green-500/10 p-4">

                <FaBrain className="text-3xl text-green-400" />

              </div>

              <div>

                <p className="text-slate-400">

                  Technical Score

                </p>

                <h2 className="text-5xl font-bold text-green-400">

                  {technical_score}%

                </h2>

              </div>

            </div>

          </div>

          <div className="rounded-3xl border border-cyan-500/20 bg-[#08111f] p-8">

            <div className="flex items-center gap-4">

              <div className="rounded-full bg-yellow-500/10 p-4">

                <FaComments className="text-3xl text-yellow-400" />

              </div>

              <div>

                <p className="text-slate-400">

                  Communication

                </p>

                <h2 className="text-5xl font-bold text-yellow-400">

                  {communication_score}%

                </h2>

              </div>

            </div>

          </div>

        </div>

        {/* PART 2 STARTS HERE */}
                {/* Topic-wise Performance */}

        <div className="mt-10 rounded-3xl border border-cyan-500/20 bg-[#08111f] p-8">

          <h2 className="mb-8 text-3xl font-bold">

            Topic-wise Performance

          </h2>

          {Object.keys(topic_scores || {}).length === 0 ? (

            <p className="text-slate-400">

              No topic-wise analysis available.

            </p>

          ) : (

            <div className="space-y-6">

              {Object.entries(topic_scores).map(

                ([topic, score]) => (

                  <div key={topic}>

                    <div className="mb-2 flex justify-between">

                      <span className="font-semibold">

                        {topic}

                      </span>

                      <span className="text-cyan-400">

                        {score}%

                      </span>

                    </div>

                    <div className="h-3 overflow-hidden rounded-full bg-slate-700">

                      <div

                        className="h-full rounded-full bg-cyan-400 transition-all duration-700"

                        style={{

                          width: `${score}%`

                        }}

                      />

                    </div>

                  </div>

                )

              )}

            </div>

          )}

        </div>

        {/* Strengths & Weaknesses */}

        <div className="mt-10 grid gap-8 lg:grid-cols-2">

          {/* Strengths */}

          <div className="rounded-3xl border border-green-500/20 bg-[#08111f] p-8">

            <div className="mb-6 flex items-center gap-3">

              <FaCheckCircle className="text-3xl text-green-400" />

              <h2 className="text-3xl font-bold">

                Strengths

              </h2>

            </div>

            {strengths && strengths.length > 0 ? (

              <div className="space-y-4">

                {strengths.map(

                  (item, index) => (

                    <div

                      key={index}

                      className="rounded-xl border border-green-500/20 bg-green-500/5 p-4"

                    >

                      {item}

                    </div>

                  )

                )}

              </div>

            ) : (

              <p className="text-slate-400">

                No strengths available.

              </p>

            )}

          </div>

          {/* Weaknesses */}

          <div className="rounded-3xl border border-red-500/20 bg-[#08111f] p-8">

            <div className="mb-6 flex items-center gap-3">

              <FaChartBar className="text-3xl text-red-400" />

              <h2 className="text-3xl font-bold">

                Areas for Improvement

              </h2>

            </div>

            {weaknesses && weaknesses.length > 0 ? (

              <div className="space-y-4">

                {weaknesses.map(

                  (item, index) => (

                    <div

                      key={index}

                      className="rounded-xl border border-red-500/20 bg-red-500/5 p-4"

                    >

                      {item}

                    </div>

                  )

                )}

              </div>

            ) : (

              <p className="text-slate-400">

                No improvement areas available.

              </p>

            )}

          </div>

        </div>

        {/* PART 3 STARTS HERE */}
                {/* Hiring Recommendation */}

        <div className="mt-10 rounded-3xl border border-cyan-500/20 bg-[#08111f] p-8">

          <h2 className="mb-8 text-3xl font-bold">

            Hiring Recommendation

          </h2>

          <div className="grid gap-8 lg:grid-cols-2">

            <div>

              <h3 className="text-lg text-slate-400">

                Recommendation

              </h3>

              <div className="mt-3 inline-flex rounded-full bg-cyan-500/10 px-6 py-3 text-2xl font-bold text-cyan-400">

                {recommendation?.recommendation || "Not Available"}

              </div>

            </div>

            <div>

              <h3 className="text-lg text-slate-400">

                Confidence

              </h3>

              <p className="mt-3 text-4xl font-bold text-green-400">

                {recommendation?.confidence || 0}%

              </p>

            </div>

          </div>

          <div className="mt-8">

            <h3 className="mb-3 text-xl font-semibold">

              AI Feedback

            </h3>

            <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6 leading-8 text-slate-300">

              {recommendation?.reason ||

                "No recommendation generated."}

            </div>

          </div>

        </div>

        {/* Learning Roadmap */}

        <div className="mt-10 rounded-3xl border border-cyan-500/20 bg-[#08111f] p-8">

          <h2 className="mb-8 text-3xl font-bold">

            Personalized Learning Roadmap

          </h2>

          {learning_roadmap &&
          Object.keys(learning_roadmap).length > 0 ? (

            <div className="space-y-8">

              {Object.entries(learning_roadmap).map(

                ([topic, items]) => (

                  <div
                    key={topic}
                    className="rounded-2xl border border-cyan-500/20 p-6"
                  >

                    <h3 className="mb-5 text-2xl font-bold text-cyan-400">

                      {topic}

                    </h3>

                    {Array.isArray(items) ? (

                      <ul className="space-y-3">

                        {items.map((item, index) => (

                          <li
                            key={index}
                            className="rounded-xl bg-slate-800 p-4"
                          >

                            • {item}

                          </li>

                        ))}

                      </ul>

                    ) : (

                      <pre className="whitespace-pre-wrap text-slate-300">

                        {JSON.stringify(items, null, 2)}

                      </pre>

                    )}

                  </div>

                )

              )}

            </div>

          ) : (

            <p className="text-slate-400">

              No learning roadmap available.

            </p>

          )}

        </div>

        {/* PART 4 STARTS HERE */}
                {/* Action Buttons */}

        <div className="mt-12 flex flex-wrap justify-center gap-6">

          <button
            onClick={() => navigate("/interview")}
            className="rounded-2xl bg-cyan-400 px-8 py-4 font-bold text-black transition hover:scale-105"
          >
            <FaMicrophone className="mr-3 inline" />
            Take Another Interview
          </button>

          <button
            onClick={() => navigate("/dashboard")}
            className="rounded-2xl border border-cyan-500/20 px-8 py-4 font-bold transition hover:bg-cyan-500/10"
          >
            <FaArrowLeft className="mr-3 inline" />
            Back to Dashboard
          </button>

          <button
            disabled
            className="cursor-not-allowed rounded-2xl border border-slate-600 px-8 py-4 font-bold text-slate-500"
          >
            Download PDF (Coming Soon)
          </button>

        </div>

      </div>

    </div>

  );

}