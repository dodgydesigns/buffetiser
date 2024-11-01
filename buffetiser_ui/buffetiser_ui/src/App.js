import { useState, useEffect } from "react";
import axios from "axios";

import MenuBar from "./components/menu_bar";
import InvestmentCard from "./components/investment_card";
import TotalsCard from "./components/totals_card";

import "./index.css";

function InvestmentCards({ allInvestments }) {
  return (
    <div className="investment_cards_container">
      {allInvestments.map((item) => InvestmentCard(item))};
    </div>
  );
}

/*
Pull all (most?) of the required information once and feed it to
the child components.
*/
export default function App() {
  const [allInvestments, setAllInvestments] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/all")
      .then((response) => {
        setAllInvestments(response.data.all_investment_data);
      })
      .catch((error) => {
        console.log(error.response);
      });
  }, []);

  return (
    <>
      <MenuBar />
      <div className="content">
        {" "}
        <InvestmentCards allInvestments={allInvestments} />
      </div>
      <footer className="footer">
        <TotalsCard />
      </footer>
    </>
  );
}
