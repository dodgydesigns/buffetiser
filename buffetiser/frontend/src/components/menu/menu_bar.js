import { useState } from "react";
import NewInvestmentModal from "./new_investment_modal.js";
import ConfigModal from "./config_modal.js";
import axios from "axios";
import "../../index.css";

const baseURL = "http://127.0.0.1:8000";

function MenuBar(constants) {
  const [showNewInvestment, setShowNewInvestment] = useState(false);
  const [showConfig, setShowConfig] = useState(false);

  const handleNewInvestmentClose = () => {
    setShowNewInvestment(false);
  };

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
          setShowNewInvestment(true);
        }}
      >
        {showNewInvestment && (
          <NewInvestmentModal
            props={constants}
            endpoint={baseURL + "/new_investment/"}
            onClose={() => handleNewInvestmentClose()}
          ></NewInvestmentModal>
        )}
        New Investment
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          axios.get(baseURL + "/reports/");
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
    </div>
  );
}

export default MenuBar;
