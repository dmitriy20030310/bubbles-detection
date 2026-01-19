// frontend/src/components/Sidebar/Sidebar.js
import { NavLink } from "react-router-dom";
import { useState } from "react";
import "./Sidebar.css";

const Sidebar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Закрываем меню при клике на ссылку
  const handleLinkClick = () => {
    setIsMenuOpen(false);
  };

  return (
    <header className="sidebar-header">
      <div className="sidebar-brand">
        <h1>Детектор пузырей</h1>
      </div>

      {/* Гамбургер-иконка (только на мобильных) */}
      <button
        className="menu-toggle"
        onClick={() => setIsMenuOpen(!isMenuOpen)}
        aria-label={isMenuOpen ? "Close menu" : "Open menu"}
      >
        {isMenuOpen ? "✖" : "☰"}
      </button>

      {/* Навигация */}
      <nav className={isMenuOpen ? "nav-mobile open" : "nav-mobile"}>
        <ul>
          <li><NavLink to="/description" onClick={handleLinkClick}>О проекте</NavLink></li>
          <li><NavLink to="/test-model" onClick={handleLinkClick}>Тестирование детектора</NavLink></li>
        </ul>
      </nav>
    </header>
  );
};

export default Sidebar;
