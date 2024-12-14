import { useState } from "react";
import PopupModal from "./new_investment_modal.js";
import axios from "axios";
import "../../index.css";

const baseURL = "http://127.0.0.1:8000";

function MenuBar(constants) {
  const [showNewInvestment, setShowNewInvestment] = useState(false);

  const handleNewInvestmentClose = (ok, isOpen) => {
    setShowNewInvestment(isOpen);
  };

  return (
    <div className="header">
      <span
        className="header_bar_div"
        onClick={() => {
          axios.request(baseURL + "/config/");
        }}
      >
        Configuration
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          setShowNewInvestment(true);
        }}
      >
        {showNewInvestment && (
          <PopupModal
            props={constants}
            endpoint={baseURL + "/new_investment/"}
            onClose={() => handleNewInvestmentClose()}
          ></PopupModal>
        )}
        New Investment
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          axios.post(baseURL + "/reports/");
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
