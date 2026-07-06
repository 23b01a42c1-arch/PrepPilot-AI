import { FaExclamationTriangle } from "react-icons/fa";

export default function ExitInterviewModal({
  open,
  onCancel,
  onConfirm,
  loading,
}) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">

      <div className="w-full max-w-md rounded-3xl border border-cyan-500/20 bg-[#08111f] p-8 shadow-2xl">

        <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-red-500/10">

          <FaExclamationTriangle className="text-4xl text-red-400" />

        </div>

        <h2 className="mt-6 text-center text-3xl font-bold text-white">

          Exit Interview?

        </h2>

        <p className="mt-4 text-center leading-7 text-slate-400">

          Your interview will end now.

          <br />

          A detailed report will be generated using only the
          questions you've answered so far.

        </p>

        <div className="mt-10 flex gap-4">

          <button
            onClick={onCancel}
            disabled={loading}
            className="flex-1 rounded-2xl border border-cyan-500/20 py-3 font-semibold text-white transition hover:bg-cyan-500/10"
          >
            Continue Interview
          </button>

          <button
            onClick={onConfirm}
            disabled={loading}
            className="flex-1 rounded-2xl bg-red-500 py-3 font-semibold text-white transition hover:bg-red-600"
          >
            {loading ? "Generating..." : "Exit & Report"}
          </button>

        </div>

      </div>

    </div>
  );
}