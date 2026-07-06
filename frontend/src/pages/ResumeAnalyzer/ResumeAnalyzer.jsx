import { useState } from "react";
import { FaCloudUploadAlt, FaFileAlt, FaRocket } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import api from "../../api/axios";

export default function ResumeAnalyzer() {
  const navigate = useNavigate();

  const [resume, setResume] = useState(null);
  const [jdText, setJdText] = useState("");
  const [loading, setLoading] = useState(false);

  const analyzeResume = async () => {
    if (!resume) {
      alert("Please upload your resume.");
      return;
    }

    if (!jdText.trim()) {
      alert("Please paste the Job Description.");
      return;
    }

    try {
      setLoading(true);

      // Upload Resume
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

      // Analyze Resume
      const response = await api.post(
        "/resume/analyze",
        {
          resume_filename: resumeFilename,
          jd_text: jdText,
        }
      );

      navigate("/resume/analysis", {
        state: response.data,
      });

    } catch (err) {
      console.log(err);
      alert("Failed to analyze resume.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#020817] flex justify-center items-center px-6 py-12">

      <div className="w-full max-w-5xl rounded-3xl border border-orange-500/20 bg-[#0F172A] p-10 shadow-2xl">

        <h1 className="text-5xl font-bold text-white">
          AI Resume Analyzer
        </h1>

        <p className="mt-3 text-slate-400 text-lg">
          Upload your resume and compare it with a Job Description.
        </p>

        <div className="mt-10 grid md:grid-cols-2 gap-8">

          {/* Resume Upload */}

          <div>

            <label className="text-white font-semibold flex items-center gap-3 mb-4">

              <FaCloudUploadAlt className="text-orange-400 text-xl"/>

              Upload Resume

            </label>

            <label
              className="cursor-pointer flex flex-col items-center justify-center h-72 rounded-3xl border-2 border-dashed border-orange-500/30 hover:border-orange-400 transition"
            >

              <FaFileAlt
                className="text-6xl text-orange-400"
              />

              <p className="mt-5 text-slate-300">

                Click to Upload PDF

              </p>

              <p className="text-sm text-slate-500 mt-2">

                PDF only

              </p>

              <input
                hidden
                type="file"
                accept=".pdf"
                onChange={(e)=>setResume(e.target.files[0])}
              />

            </label>

            {resume && (

              <div className="mt-4 rounded-xl bg-orange-500/10 p-4 text-orange-300">

                {resume.name}

              </div>

            )}

          </div>

          {/* Job Description */}

          <div>

            <label className="text-white font-semibold mb-4 block">

              Job Description

            </label>

            <textarea

              rows={14}

              value={jdText}

              onChange={(e)=>setJdText(e.target.value)}

              placeholder="Paste complete Job Description..."

              className="h-72 w-full rounded-3xl border border-orange-500/20 bg-[#020817] p-6 text-white outline-none focus:border-orange-400"

            />

          </div>

        </div>

        <button

          onClick={analyzeResume}

          disabled={loading}

          className="mt-10 flex w-full items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-orange-500 to-orange-400 py-5 text-xl font-bold text-black transition hover:scale-[1.02] disabled:opacity-60"

        >

          <FaRocket/>

          {loading ? "Analyzing Resume..." : "Analyze Resume"}

        </button>

      </div>

    </div>
  );
}