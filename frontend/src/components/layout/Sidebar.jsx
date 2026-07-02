import {
  FaHome,
  FaMicrophone,
  FaFileAlt,
  FaHistory,
  FaChartBar,
  FaUser,
  FaCog,
  FaSignOutAlt,
} from "react-icons/fa";

import { NavLink } from "react-router-dom";

const menu = [
  {
    name: "Dashboard",
    icon: <FaHome />,
    path: "/dashboard",
  },
  {
    name: "AI Interview",
    icon: <FaMicrophone />,
    path: "/interview",
  },
  {
    name: "Resume Analyzer",
    icon: <FaFileAlt />,
    path: "/resume",
  },
  {
    name: "History",
    icon: <FaHistory />,
    path: "/history",
  },
  {
    name: "Reports",
    icon: <FaChartBar />,
    path: "/reports",
  },
  {
    name: "Profile",
    icon: <FaUser />,
    path: "/profile",
  },
  {
    name: "Settings",
    icon: <FaCog />,
    path: "/settings",
  },
];

export default function Sidebar() {
  return (
    <aside className="w-[270px] bg-[#081221] border-r border-cyan-500/10 min-h-screen p-8 flex flex-col">

      <h1 className="text-3xl font-bold">

        PrepPilot

        <span className="text-cyan-400">

          AI

        </span>

      </h1>

      <p className="text-slate-400 text-sm mt-1">

        AI Interview Coach

      </p>

      <nav className="mt-14 flex-1 space-y-3">

        {menu.map((item) => (

          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-4 rounded-xl px-5 py-4 transition ${
                isActive
                  ? "bg-cyan-500 text-black font-semibold"
                  : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >
            {item.icon}

            {item.name}

          </NavLink>

        ))}

      </nav>

      <button className="flex items-center gap-4 rounded-xl px-5 py-4 text-red-400 hover:bg-red-500/10 transition">

        <FaSignOutAlt />

        Logout

      </button>

    </aside>
  );
}