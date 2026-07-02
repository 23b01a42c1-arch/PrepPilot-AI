import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

export default function ProgressChart() {
  const data = {
    labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
    datasets: [
      {
        label: "Interview Score",
        data: [65, 72, 80, 91],
        borderColor: "#22d3ee",
        backgroundColor: "rgba(34,211,238,.2)",
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: "#ffffff",
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#94a3b8",
        },
      },
      y: {
        ticks: {
          color: "#94a3b8",
        },
      },
    },
  };

  return (
    <div className="glass rounded-3xl border border-cyan-500/20 p-8">
      <h2 className="mb-6 text-2xl font-bold">
        Interview Progress
      </h2>

      <Line
        data={data}
        options={options}
      />
    </div>
  );
}