import { useState } from "react";
import PopupModal from "./popup_modal.js";
import axios from "axios";
import "../../index.css";

const baseURL = "127.0.0.1:8000";

function MenuBar() {
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
          // axios.post(baseURL + "/new_investment/");
        }}
      >
        {showNewInvestment && (
          <PopupModal
            endpoint={"www.fuck.you.com"}
            children="`<div>Hello</div>`"
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
