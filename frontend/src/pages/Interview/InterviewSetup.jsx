import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  FaBriefcase,
  FaLayerGroup,
  FaListOl,
  FaMicrophone,
  FaKeyboard,
  FaFileUpload,
} from "react-icons/fa";

import Button from "../../components/common/Button";
import api from "../../api/axios";

export default function InterviewSetup() {
  const navigate = useNavigate();

  const [role, setRole] = useState("");
  const [difficulty, setDifficulty] = useState("Medium");
  const [questions, setQuestions] = useState(10);
  const [mode, setMode] = useState("text");

  const [resume, setResume] = useState(null);
  const [jdText, setJdText] = useState("");

  const [loading, setLoading] = useState(false);

  const handleStart = async () => {
    if (!resume) {
      alert("Please upload your resume.");
      return;
    }

    if (!jdText.trim()) {
      alert("Please enter the Job Description.");
      return;
    }

    try {
      setLoading(true);

      // ---------------- Upload Resume ----------------

      const formData = new FormData();
      formData.append("file", resume);

      const uploadResponse = await api.post(
        "/resume/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const resumeFilename = uploadResponse.data.filename;

      // ---------------- Generate Interview ----------------

      const interviewResponse = await api.post(
        "/interview/generate",
        {
          resume_filename: resumeFilename,
          jd_text: jdText,
        }
      );

      const data = interviewResponse.data;

      navigate("/interview/session", {
        state: {
          sessionId: data.session_id,
          firstQuestion: data.first_question.question,
          firstAudio: data.first_question.audio,
          role,
          difficulty,
          questions,
        },
      });
    } catch (error) {
      console.error(error);

      alert(
        error.response?.data?.error ||
          "Unable to generate interview."
      );
    } finally {
      setLoading(false);
    }
  };

  return (    <div className="min-h-screen bg-[#020817] flex items-center justify-center px-6 py-10">

      <div className="glass w-full max-w-4xl rounded-3xl border border-cyan-500/20 p-10">

        <h1 className="text-4xl font-bold text-white">
          AI Interview Setup
        </h1>

        <p className="mt-3 text-slate-400">
          Upload your resume and job description to generate a personalized AI interview.
        </p>

        <div className="mt-10 space-y-6">

          {/* Resume Upload */}

          <div>

            <label className="mb-2 flex items-center gap-2 text-slate-300">
              <FaFileUpload className="text-cyan-400" />
              Upload Resume (PDF)
            </label>

            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResume(e.target.files[0])}
              className="w-full rounded-xl border border-cyan-500/20 bg-[#0F172A] p-4 text-white"
            />

          </div>

          {/* Job Description */}

          <div>

            <label className="mb-2 block text-slate-300">
              Job Description
            </label>

            <textarea
              rows={8}
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
              placeholder="Paste the complete Job Description here..."
              className="w-full rounded-xl border border-cyan-500/20 bg-[#0F172A] p-4 text-white outline-none focus:border-cyan-400"
            />

          </div>

          {/* Job Role */}

          <input
            type="text"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            placeholder="e.g. AI/ML Engineer"
            className="glass w-full rounded-xl border border-cyan-500/20 bg-transparent p-4 text-white placeholder:text-slate-500 outline-none"
          />

          {/* Difficulty */}

          <div>

            <label className="mb-2 flex items-center gap-2 text-slate-300">
              <FaLayerGroup className="text-cyan-400" />
              Difficulty
            </label>

            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="glass w-full rounded-xl border border-cyan-500/20 bg-transparent p-4 text-white"
            >
              <option className="bg-slate-900">Easy</option>
              <option className="bg-slate-900">Medium</option>
              <option className="bg-slate-900">Hard</option>
            </select>

          </div>

          {/* Questions */}

          <div>

            <label className="mb-2 flex items-center gap-2 text-slate-300">
              <FaListOl className="text-cyan-400" />
              Number of Questions
            </label>

            <select
              value={questions}
              onChange={(e) => setQuestions(Number(e.target.value))}
              className="glass w-full rounded-xl border border-cyan-500/20 bg-transparent p-4 text-white"
            >
              <option className="bg-slate-900" value={5}>5</option>
              <option className="bg-slate-900" value={10}>10</option>
              <option className="bg-slate-900" value={15}>15</option>
            </select>

          </div>

          {/* Interview Mode */}

          

        

          <Button
            className="mt-8 w-full"
            onClick={handleStart}
            disabled={loading}
          >
            {loading ? "Generating Interview..." : "Start AI Interview →"}
          </Button>

        </div>

      </div>

    </div>
  );
}
