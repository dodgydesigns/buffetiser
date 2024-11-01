function PositiveColour(comparisonValue) {
  return comparisonValue >= 0 ? "#55ff55" : "#ff4444";
}

/*  Show the total value of the portfolio and percentage gain. */
export default function TotalsHeader({ totalPortfolioValues }) {
  const valueColour = PositiveColour(totalPortfolioValues.total_profit);
  return (
    <>
      <table className="totals_header">
        <tbody>
          <tr>
            <td width="10%">PORTFOLIO</td>
            <td style={{ color: valueColour }} width="10%">
              ${totalPortfolioValues.total_profit.toFixed(2)}
            </td>
            <td style={{ color: valueColour }}>
              {totalPortfolioValues.total_profit_percentage.toFixed(2)}%
            </td>
          </tr>
        </tbody>
      </table>
    </>
  );
}
