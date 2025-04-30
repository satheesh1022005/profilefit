import React from "react";
import { FaUpload } from "react-icons/fa";

function OpportunityInput({ value, onChange, onUpload }) {
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
      <h3>Job Description</h3>
      <div className="textarea-wrapper">
        <textarea
          name="opportunity"
          value={value}
          onChange={onChange}
          placeholder="Paste job description here..."
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

export default OpportunityInput;