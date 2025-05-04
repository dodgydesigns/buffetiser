import { useState } from "react";
import { useNavigate } from 'react-router-dom';
import NewInvestmentModal from "./new_investment_modal.js";
import NewReinvestmentModal from "./new_reinvestment_modal.js";
import NewDividendModal from "./new_dividend_modal.js";
import ConfigModal from "./config_modal.js";
import axios from "axios";
import "../../index.css";

const baseURL = "http://localhost:8000";

function MenuBar(constants) {
  const [showNewInvestment, setShowNewInvestment] = useState(false);
  const [showNewReinvestment, setShowNewReinvestment] = useState(false);
  const [showNewDividend, setShowNewDividend] = useState(false);
  const [showConfig, setShowConfig] = useState(false);
  const [newDropdownOpen, setNewDropdownOpen] = useState(false);
  const navigate = useNavigate();

  const handleNewDropdownOpen = () => {
    setNewDropdownOpen(!newDropdownOpen);
  };

  const handleNewInvestment = () => {
    setShowNewInvestment(true);
  }
  const handleNewInvestmentClose = () => {
    setShowNewInvestment(false);
  };
  const handleNewReinvestment = () => {
    setShowNewReinvestment(true);
  }
  const handleNewReinvestmentClose = () => {
    setShowNewReinvestment(false);
  };
  const handleNewDividend = () => {
    setShowNewDividend(true);
  }
  const handleNewDividendClose = () => {
    setShowNewDividend(false);
  }

  const handleConfigClose = () => {
    setShowConfig(false);
  };

  return (
    <div className="header">
      <span
        className="header_bar_div"
        onClick={() => {
          setShowConfig(true);
        }}
      >
        {showConfig && (
          <ConfigModal
            props={constants}
            baseURL={baseURL}
            onClose={() => handleConfigClose()}
          ></ConfigModal>
        )}
        Admin
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          handleNewDropdownOpen();
        }}
      >
        {newDropdownOpen && (
          <ul className="menu">
            <li className="menu-item">
              <button onClick={handleNewInvestment}>Investment</button>
            </li>
            <li className="menu-item">
              <button onClick={handleNewReinvestment}>Reinvestment</button>
            </li>
            <li className="menu-item">
              <button onClick={handleNewDividend}>Dividend</button>
            </li>
          </ul>
        )}
        {showNewInvestment && (
          <NewInvestmentModal
            props={constants}
            endpoint={baseURL + "/new_investment/"}
            onClose={() => handleNewInvestmentClose()}
          ></NewInvestmentModal>
        )}
        {showNewReinvestment && (
          <NewReinvestmentModal
            props={constants}
            endpoint={baseURL + "/add_reinvestment/"}
            onClose={() => handleNewReinvestmentClose()}
          ></NewReinvestmentModal>
        )}
        {showNewDividend && (
          <NewDividendModal
            props={constants}
            endpoint={baseURL + "/add_dividend/"}
            onClose={() => handleNewDividendClose()}
          ></NewDividendModal>
        )}
        Add New
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          navigate("/reports/");
        }}
      >
        Reports
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          axios.post(baseURL + "/help/");
        }}
      >
        Help
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          const refreshToken = localStorage.getItem("refresh_token");
          if (!refreshToken) {
            alert("No refresh token found. Please log in again.");
            navigate('/login/');
            return;
          }

          axios.post(baseURL + "/logout/", { refresh_token: refreshToken }, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
          }).then(() => {
            localStorage.removeItem("access_token"); // Remove access token
            localStorage.removeItem("refresh_token"); // Remove refresh token
            navigate('/login/');
          }).catch((error) => {
            if (error.response && error.response.status === 400) {
              alert("Invalid or expired refresh token. Please log in again.");
            } else {
              console.error("Logout failed:", error);
              alert("Are you sure you want to leave this awesome App?");
            }
            navigate('/login/');
          });
        }}
      >
        Logout
      </span>
    </div>
  );
}

export default MenuBar;
