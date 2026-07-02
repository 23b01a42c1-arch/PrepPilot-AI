export default function RecentInterviews() {

  return (
    <div className="glass rounded-3xl border border-cyan-500/20 p-8">

      <h2 className="mb-6 text-2xl font-bold">

        Recent Interviews

      </h2>

      <div className="flex h-52 items-center justify-center rounded-2xl border border-dashed border-cyan-500/20">

        <div className="text-center">

          <h3 className="text-xl font-semibold">

            No Interviews Yet

          </h3>

          <p className="mt-3 text-slate-400">

            Complete your first AI interview to see your history here.

          </p>

        </div>

      </div>

    </div>
  );
}