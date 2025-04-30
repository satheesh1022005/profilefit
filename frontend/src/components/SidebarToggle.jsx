import React from 'react';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';

function SidebarToggle({ isCollapsed, onClick }) {
  return (
    <button
      className="sidebar-toggle"
      onClick={onClick}
      title={isCollapsed ? "Show Keywords" : "Hide Keywords"}
    >
      {isCollapsed ? <FaChevronLeft /> : <FaChevronRight />}
    </button>
  );
}

export default SidebarToggle;