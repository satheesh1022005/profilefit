import React from "react";
import { FaUpload } from "react-icons/fa"; // Install react-icons if not installed

function ResumeInput({ value, onChange, onUpload }) {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/pdf") {
      onUpload(file);
    } else {
      alert("Please select a valid PDF file.");
    }
  };

  return (
    <div className="input-group">
      <h3>Resume</h3>
      <div className="textarea-wrapper">
        <textarea
          name="resume"
          value={value}
          onChange={onChange}
          placeholder="Paste your resume here..."
        />
        <label className="upload-icon" title="Upload PDF">
          <FaUpload />
          <input
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
          />
        </label>
      </div>
    </div>
  );
}

export default ResumeInput;