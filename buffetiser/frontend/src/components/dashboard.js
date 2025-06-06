import { useState, useEffect } from "react";
import axios from "axios";

import MenuBar from "./menu/menu_bar";
import InvestmentCard from "./investment_cards/investment_card";
import TotalsCard from "./totals_card";

import "../index.css";

function InvestmentCards({ allInvestments, constants }) {
  return (
    <div className="investment_cards_container">
      {allInvestments.map((item) => item.visible && InvestmentCard(item, constants))};
    </div>
  );
}

/*
Pull all of the required information once and feed it to
the child components.
*/
export default function Dashboard() {
  const [allInvestments, setAllInvestments] = useState([]);
  const [constants, setConstants] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/all")
      .then((response) => {
        setAllInvestments(response.data.all_investment_data);
      })
      .catch((error) => {
        console.log(error.response);
      });

    axios
      .get("http://localhost:8000/constants")
      .then((response) => {
        setConstants(response.data);
      })
      .catch((error) => {
        console.log(error.response);
      });
  }, []);

  // Make sure the data has been received.
  if (allInvestments.length === 0 || constants.length === 0) {
    return <div>Loading!</div>
  }

  return (
    <>
      <MenuBar constants={constants} />
      <div className="content">
        <InvestmentCards allInvestments={allInvestments} constants={constants}/>
      </div>
      <footer className="footer">
        <TotalsCard />
      </footer>
    </>
  );
}