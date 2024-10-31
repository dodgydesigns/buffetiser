import TotalsChart from "./totals_chart";
import TotalsHeader from "./totals_header";

/*
This hold the details showing overall changes of the portfolio over time. This 
includes a chart showing date vs (purchases and sales) and combined value of the 
whole portfolio.
*/
function TotalsCard(portfolioTotals) {
  return (
    <>
      <TotalsHeader portfolioTotals={portfolioTotals} />
      <TotalsChart />
    </>
  );
}

export default TotalsCard;
