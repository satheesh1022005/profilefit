import React from "react";
import { FaCheck, FaTimes, FaLightbulb } from "react-icons/fa";

function KeywordList({ title, keywords }) {
  const getIcon = () => {
    switch (title) {
      case "Resume Keywords":
        return <FaCheck color="#00FFC6" />;
      case "Missing Keywords":
        return <FaTimes color="#FF6363" />;
      case "Opportunity Keywords":
        return <FaLightbulb color="#9333EA" />;
      default:
        return null;
    }
  };

  return (
    <div className="keyword-list" title={title}>
      <h3>
        {getIcon()}
        {title}
      </h3>
      <ul>
        {keywords.map((word, index) => (
          <li key={index}>{word}</li>
        ))}
        {keywords.length === 0 && <li>No keywords found</li>}
      </ul>
    </div>
  );
}

export default KeywordList;