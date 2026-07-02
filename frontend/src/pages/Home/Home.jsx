import Navbar from "../../components/layout/Navbar";
import Hero from "../../components/home/Hero";
import Services from "../../components/home/Services";
import HowItWorks from "../../components/home/HowItWorks";
import Footer from "../../components/layout/Footer";

export default function Home() {
  return (
    <main className="bg-[#020817] text-white overflow-hidden">

      <Navbar />

      <Hero />

      <Services />

      <HowItWorks />

      <Footer />

    </main>
  );
}