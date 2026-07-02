import { useNavigate } from "react-router-dom";
import {
  FaMicrophone,
  FaFileAlt,
  FaChartBar,
  FaHistory,
} from "react-icons/fa";

export default function QuickActions() {

  const navigate = useNavigate();

  const actions = [
    {
      title: "Start Interview",
      icon: <FaMicrophone />,
      route: "/interview",
    },
    {
      title: "Resume Analyzer",
      icon: <FaFileAlt />,
      route: "/resume",
    },
    {
      title: "Reports",
      icon: <FaChartBar />,
      route: "/reports",
    },
    {
      title: "History",
      icon: <FaHistory />,
      route: "/history",
    },
  ];

  return (
    <div className="glass rounded-3xl border border-cyan-500/20 p-8">

      <h2 className="mb-6 text-2xl font-bold">

        Quick Actions

      </h2>

      <div className="grid grid-cols-2 gap-5">

        {actions.map((action) => (

          <button
            key={action.title}
            onClick={() => navigate(action.route)}
            className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6 transition duration-300 hover:border-cyan-400 hover:bg-cyan-500/10 hover:scale-[1.03]"
          >

            <div className="mb-4 text-4xl text-cyan-400">

              {action.icon}

            </div>

            <h3 className="text-lg font-semibold">

              {action.title}

            </h3>

          </button>

        ))}

      </div>

    </div>
  );
}