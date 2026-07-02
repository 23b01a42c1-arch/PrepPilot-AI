import { useState, useRef, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  FaClock,
  FaMicrophone,
  FaStop,
  FaVolumeUp,
} from "react-icons/fa";

import api from "../../api/axios";

export default function InterviewSession() {
  const navigate = useNavigate();

  const { state } = useLocation();

  const {
    sessionId,
    firstQuestion,
    role,
    difficulty,
    questions,
    firstAudio,
} = state || {};

  const [question, setQuestion] = useState(
    firstQuestion || "Loading..."
  );

  const [questionNumber, setQuestionNumber] = useState(1);

  const [recording, setRecording] = useState(false);

  const [loading, setLoading] = useState(false);

  const [transcript, setTranscript] = useState("");

  const [audioUrl, setAudioUrl] = useState("");

  const mediaRecorder = useRef(null);

  const audioChunks = useRef([]);

  const audioPlayer = useRef(null);

  useEffect(() => {

    async function requestMicPermission() {

      try {

        await navigator.mediaDevices.getUserMedia({
          audio: true,
        });

      } catch (err) {

        alert("Please allow microphone access.");

      }

    }

    requestMicPermission();

  }, []);
  useEffect(() => {

  if (firstAudio) {

    setAudioUrl(
      `http://127.0.0.1:8000${firstAudio}?t=${Date.now()}`
    );

  }

}, [firstAudio]);

  useEffect(() => {

    if (audioUrl && audioPlayer.current) {

      audioPlayer.current.play();

    }

  }, [audioUrl]);
    const startRecording = async () => {

    try {

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      mediaRecorder.current = new MediaRecorder(stream);

      audioChunks.current = [];

      mediaRecorder.current.ondataavailable = (event) => {

        if (event.data.size > 0) {

          audioChunks.current.push(event.data);

        }

      };

      mediaRecorder.current.start();

      setRecording(true);

    } catch (err) {

      console.error(err);

      alert("Unable to access microphone.");

    }

  };

  const stopRecording = async () => {

    setRecording(false);

    mediaRecorder.current.stop();

    mediaRecorder.current.onstop = async () => {

      try {

        setLoading(true);

        const audioBlob = new Blob(
          audioChunks.current,
          {
            type: "audio/webm",
          }
        );

        const formData = new FormData();

        const filename = `answer_${Date.now()}.webm`;

        formData.append(
          "file",
          audioBlob,
          filename
        );

        // ---------------- Upload Audio ----------------

        const uploadResponse =
          await api.post(
            "/voice/upload",
            formData,
            {
              headers: {
                "Content-Type":
                  "multipart/form-data",
              },
            }
          );

        // ---------------- Evaluate Answer ----------------

        const answerResponse =
          await api.post(
            "/voice/answer",
            {
              session_id: sessionId,
              audio_filename:
                uploadResponse.data.path,
            }
          );

        const data = answerResponse.data;

        setTranscript(
          data.transcript
        );

        if (data.type === "completed") {

          alert("Interview Completed!");

          navigate("/report", {
            state: {
              sessionId,
            },
          });

          return;

        }

        setQuestion(
          data.question
        );

        setQuestionNumber(
          (prev) => prev + 1
        );

        if (data.audio) {

          setAudioUrl(
            `http://127.0.0.1:8000${data.audio}?t=${Date.now()}`
          );

        }

      } catch (err) {

        console.error(err);

        alert(
          "Failed to process interview answer."
        );

      } finally {

        setLoading(false);

      }

    };

  };
    return (
    <div className="min-h-screen bg-[#020817] text-white">

      {/* Hidden audio player */}
      <audio
        ref={audioPlayer}
        src={audioUrl}
      />

      {/* Header */}

      <div className="border-b border-cyan-500/20 bg-[#08111f] px-10 py-6">

        <div className="flex items-center justify-between">

          <div>

            <h1 className="text-3xl font-bold">
              PrepPilot AI Interview
            </h1>

            <p className="mt-2 text-slate-400">
              {role} • {difficulty}
            </p>

          </div>

          <div className="glass flex items-center gap-3 rounded-2xl px-5 py-3">

            <FaClock className="text-cyan-400" />

            <span>
              Question {questionNumber}
            </span>

          </div>

        </div>

      </div>

      {/* Main */}

      <div className="mx-auto mt-10 max-w-5xl px-6">

        {/* AI Question */}

        <div className="rounded-3xl border border-cyan-500/20 bg-[#08111f] p-8">

          <div className="mb-4 flex items-center gap-3">

            <FaVolumeUp className="text-2xl text-cyan-400" />

            <h2 className="text-2xl font-bold">

              AI Interviewer

            </h2>

          </div>

          <p className="text-xl leading-9">

            {question}

          </p>

        </div>

        {/* Recording */}

        <div className="mt-10 rounded-3xl border border-cyan-500/20 bg-[#08111f] p-8">

          <h2 className="mb-6 text-2xl font-bold">

            Your Answer

          </h2>

          <div className="flex justify-center">

            {!recording ? (

              <button

                onClick={startRecording}

                disabled={loading}

                className="flex h-36 w-36 items-center justify-center rounded-full bg-cyan-500 text-5xl text-black transition hover:scale-110 disabled:opacity-50"

              >

                <FaMicrophone />

              </button>

            ) : (

              <button

                onClick={stopRecording}

                className="flex h-36 w-36 animate-pulse items-center justify-center rounded-full bg-red-500 text-5xl"

              >

                <FaStop />

              </button>

            )}

          </div>

          <p className="mt-6 text-center text-lg text-slate-400">

            {recording
              ? "Recording... Click Stop when finished."
              : "Click the microphone to start speaking."}

          </p>

          {loading && (

            <div className="mt-6 text-center text-cyan-400">

              Processing your answer...

            </div>

          )}

        </div>

        {/* Transcript */}

        {transcript && (

          <div className="mt-10 rounded-3xl border border-cyan-500/20 bg-[#08111f] p-8">

            <h2 className="mb-4 text-xl font-bold">

              Transcript

            </h2>

            <p className="leading-8 text-slate-300">

              {transcript}

            </p>

          </div>

        )}

      </div>

    </div>
  );
}