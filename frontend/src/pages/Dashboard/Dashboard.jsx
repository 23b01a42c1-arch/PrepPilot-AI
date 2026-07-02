import { useEffect, useState } from "react";
import {
  FaMicrophone,
  FaChartLine,
  FaFileAlt,
  FaTrophy,
} from "react-icons/fa";

import Sidebar from "../../components/layout/Sidebar";
import WelcomeBanner from "../../components/dashboard/WelcomeBanner";
import StatsCard from "../../components/dashboard/StatsCard";
import QuickActions from "../../components/dashboard/QuickActions";
import RecentInterviews from "../../components/dashboard/RecentInterviews";
import ProgressChart from "../../components/dashboard/ProgressChart";

import api from "../../api/axios";

export default function Dashboard() {

  const [user, setUser] = useState(null);

  useEffect(() => {

    const loadUser = async () => {

      try {

        const response = await api.get("/auth/me");

        setUser(response.data);

      } catch {

        localStorage.removeItem("token");

        window.location.href = "/login";

      }

    };

    loadUser();

  }, []);

  return (

    <div className="flex min-h-screen bg-[#020817] text-white">

      <Sidebar />

      <main className="flex-1 overflow-y-auto p-10">

        <WelcomeBanner user={user} />

        <div className="mt-8 grid grid-cols-4 gap-6">

          <StatsCard
            title="Total Interviews"
            value="0"
            icon={<FaMicrophone />}
          />

          <StatsCard
            title="Average Score"
            value="0%"
            icon={<FaChartLine />}
          />

          <StatsCard
            title="Resume Score"
            value="0%"
            icon={<FaFileAlt />}
          />

          <StatsCard
            title="Completed"
            value="0"
            icon={<FaTrophy />}
          />

        </div>

        <div className="mt-8 grid grid-cols-2 gap-6">

          <QuickActions />

          <ProgressChart />

        </div>

        <div className="mt-8">

          <RecentInterviews />

        </div>

      </main>

    </div>

  );

}