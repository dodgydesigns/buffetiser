import { useState, useEffect } from "react";
import axios from "axios";
import InvestmentCard from "./investment_card";
// import "../index.css";

export default function InvestmentCards() {
  const [allInvestments, setAllInvestments] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/all")
      .then((response) => {
        setAllInvestments(response.data.all_investment_data);
      })
      .catch((error) => {
        console.log(error.response);
      });
  }, []);

  return (
    <div className="investment_cards_container">
      {allInvestments.map((item) => InvestmentCard(item))};
    </div>
  );
}
