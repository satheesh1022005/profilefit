import React, { useState } from "react";
import axiosHeader from "../utils/axiosHeader";
import fileUploadAxios from "../utils/fileUploadAxios";
import Swal from "sweetalert2";
import Loader from "../utils/Loader";
import ResumeInput from "./ResumeInput";
import OpportunityInput from "./OpportunityInput";
import KeywordList from "./KeywordList";
import "./Dashboard.css";
import { FaUpload } from "react-icons/fa";
import SidebarToggle from './SidebarToggle';

function Dashboard() {
  const [data, setData] = useState({ resume: "", opportunity: "" });
  const [result, setResult] = useState({
    matchPercentage: null,
    missingKeywords: [],
    resumeKeywords: [],
    opportunityKeywords: []
  });
  const [loading, setLoading] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const [cache, setCache] = useState({
    resumeText: "",
    opportunityText: "",
    resumeSkills: [],
    opportunitySkills: []
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  const extractSkillsIfNeeded = async (text, type) => {
    if (type === "resume" && text === cache.resumeText) {
      return cache.resumeSkills;
    }
    if (type === "opportunity" && text === cache.opportunityText) {
      return cache.opportunitySkills;
    }

    const response = await axiosHeader.post("/extract", { resume: text });
    const skills = response.data.skills || [];

    setCache((prevCache) => ({
      ...prevCache,
      [`${type}Text`]: text,
      [`${type}Skills`]: skills
    }));

    return skills;
  };

  // Add SweetAlert dark theme configuration
  const swalDarkTheme = Swal.mixin({
    background: '#1E1E1E',
    color: '#E0E0E0',
    confirmButtonColor: '#00FFC6',
    iconColor: '#00FFC6'
  });

  // Update the submitData function to use dark themed alert
  const submitData = async (e) => {
    e.preventDefault();

    const { resume, opportunity } = data;

    if (!resume.trim() || !opportunity.trim()) {
      swalDarkTheme.fire({
        icon: "warning",
        title: "Missing fields!",
        text: "Both Resume and Opportunity fields are required."
      });
      return;
    }

    setLoading(true);

    try {
      const predictRes = await axiosHeader.post("/predict", data);
      const missingRes = await axiosHeader.post("/missing_keywords", data);

      const resumeSkills = await extractSkillsIfNeeded(resume, "resume");
      const opportunitySkills = await extractSkillsIfNeeded(opportunity, "opportunity");

      setResult({
        matchPercentage: predictRes.data.match_percentage,
        missingKeywords: missingRes.data.missing_keywords,
        resumeKeywords: resumeSkills,
        opportunityKeywords: opportunitySkills
      });

      swalDarkTheme.fire({
        icon: "success",
        title: "Profile analyzed!",
        text: "Match score and keyword insights updated."
      });
    } catch (error) {
      console.error(error);
      swalDarkTheme.fire({
        icon: "error",
        title: "Something went wrong",
        text: "Could not process the data. Please check your inputs and try again."
      });
    } finally {
      setLoading(false);
    }
  };

  // inside Dashboard function
  const uploadResumePDF = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await fileUploadAxios.post("/extract_text_from_pdf", formData);
      setData((prev) => ({ ...prev, resume: res.data.text }));
    } catch (err) {
      console.error(err);
      Swal.fire("Error extracting text from PDF.");
    } finally {
      setLoading(false);
    }
  };

  const uploadOpportunityPDF = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await fileUploadAxios.post("/extract_text_from_pdf", formData);
      setData((prev) => ({ ...prev, opportunity: res.data.text }));
    } catch (err) {
      console.error(err);
      Swal.fire("Error extracting text from PDF.");
    } finally {
      setLoading(false);
    }
  };

  const resultAvailable = result.matchPercentage !== null;

  const calculateCircleProps = () => {
    // Base values for the largest screen
    let size = 150;

    // Adjust size based on window width
    if (window.innerWidth <= 575) {
      size = 80;
    } else if (window.innerWidth <= 767) {
      size = 100;
    } else if (window.innerWidth <= 991) {
      size = 120;
    }

    const center = size / 2;
    const radius = (size / 2) * 0.9; // 90% of half the size
    const circumference = 2 * Math.PI * radius;

    return { size, center, radius, circumference };
  };

  const circleProps = calculateCircleProps();

  return (
    <div className="dashboard-container">
      {loading && <Loader />}
      <div className="form-section">
        {resultAvailable && (
          <div className="match-score">
            <div className="circular-progress">
              <svg viewBox={`0 0 ${circleProps.size} ${circleProps.size}`}>
                <circle
                  className="background"
                  cx={circleProps.center}
                  cy={circleProps.center}
                  r={circleProps.radius}
                  strokeDasharray={circleProps.circumference}
                />
                <circle
                  className="progress"
                  cx={circleProps.center}
                  cy={circleProps.center}
                  r={circleProps.radius}
                  strokeDasharray={circleProps.circumference}
                  strokeDashoffset={`${circleProps.circumference * (1 - result.matchPercentage / 100)}px`}
                />
              </svg>
              <div className="match-score-value">{result.matchPercentage}%</div>
            </div>
            <div className="match-score-details">
              <h3>Profile Match Score</h3>
              <p>Your profile matches {result.matchPercentage}% of the job requirements</p>
              <p>{result.missingKeywords.length} missing keywords identified</p>
            </div>
          </div>
        )}

        <div className="input-container">
          <ResumeInput
            value={data.resume}
            onChange={handleChange}
            onUpload={uploadResumePDF}
          />
          <OpportunityInput
            value={data.opportunity}
            onChange={handleChange}
            onUpload={uploadOpportunityPDF}
          />
        </div>

        <button onClick={submitData} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Profile"}
        </button>
      </div>

      {resultAvailable && (
        <>
          <div className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
            <KeywordList title="Resume Keywords" keywords={result.resumeKeywords} />
            <KeywordList title="Opportunity Keywords" keywords={result.opportunityKeywords} />
            <KeywordList title="Missing Keywords" keywords={result.missingKeywords} />
          </div>
          <SidebarToggle
            isCollapsed={sidebarCollapsed}
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
          />
        </>
      )}
    </div>
  );
}

export default Dashboard;
