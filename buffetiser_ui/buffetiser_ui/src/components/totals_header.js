/*  */
function TotalsHeader({ portfolioTotals }) {
  // console.log("----------------------------------");
  // console.log(portfolioTotals);
  // console.log("----------------------------------");
  return (
    <>
      <table className="totals_header">
        <tbody>
          <tr>
            <td>PORTFOLIO</td>
            <td>111 {portfolioTotals.total_profit}</td>
            <td>222 {portfolioTotals.total_profit_percentage}</td>
          </tr>
        </tbody>
      </table>
    </>
  );
}

export default TotalsHeader;
