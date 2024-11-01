import { useState, useEffect } from "react";
import axios from "axios";
import TotalsChart from "./totals_chart";
import TotalsHeader from "./totals_header";

/*
This hold the details showing overall changes of the portfolio over time. This 
includes a chart showing date vs (purchases and sales) and combined value of the 
whole portfolio.
*/
export default function TotalsCard() {
  const [totalPortfolioValues, setTotalPortfolioValues] = useState([]);
  const [portfolio_history, setPortfolio_history] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/portfolio")
      .then((response) => {
        setTotalPortfolioValues(response.data.portfolio_totals);
        setPortfolio_history(response.data.portfolio_history);
      })
      .catch((error) => {
        console.log(error.response);
      });
  }, []);

  // Make sure the data has been received.
  if (!totalPortfolioValues || portfolio_history.length === 0) {
    return null;
  }

  return (
    <>
      <TotalsHeader totalPortfolioValues={totalPortfolioValues} />
      <TotalsChart portfolio_history={portfolio_history} />
    </>
  );
}
