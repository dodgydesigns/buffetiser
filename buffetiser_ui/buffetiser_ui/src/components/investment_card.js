import React, { useState } from "react";
import InvestmentCharts from "./investment_charts";
import InvestmentSummary from "./investment_summary_panel";

function PositiveColour(comparisonValue) {
  return comparisonValue >= 0 ? "#55ff55" : "#ff4444";
}

/*
This component holds all the details of an Investment:
 - Current pricing
 - Daily changes
 - Price/Volume history chart and
 - Buttons to buy (add), sell (remove) and delete Investments
*/
function InvestmentCard(investment) {
  const [isOpen, setIsOpen] = useState(false);
  const valueColour = PositiveColour(investment.variation);

  return (
    <div key={investment.symbol}>
      {/* The 'title bar' of each Investment showing daily details of an Investment. 
          Click to show/hide the chart and summary panel */}
      <table className="card_header">
        <tbody>
          <tr onClick={() => setIsOpen((open) => !open)}>
            <td>
              <table>
                <tbody>
                  <tr>
                    <td width="40%"></td>
                    <td className="header_header" width="5%">
                      Last Price
                    </td>
                    <td className="header_header" width="5%">
                      +/-
                    </td>
                    <td className="header_header" width="5%">
                      %
                    </td>
                    <td width="6%"></td>
                    <td className="header_header" width="6%">
                      Daily Δ
                    </td>
                    <td className="header_header" width="3%">
                      +/-
                    </td>
                    <td className="header_header" width="3%">
                      %
                    </td>
                    <td className="header_header"></td>
                  </tr>
                  <tr>
                    <td>
                      <table>
                        <tbody>
                          <tr>
                            <td className="investment_symbol" width="8%">
                              {investment.symbol}
                            </td>
                            <td className="investment_name">
                              {investment.name}
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                    <td className="header_header">
                      {investment.last_price.toFixed(2)}
                    </td>
                    <td style={{ color: valueColour }}>
                      {investment.variation.toFixed(2)}
                    </td>
                    <td style={{ color: valueColour }}>
                      {investment.variation_percent.toFixed(2)}%
                    </td>
                    <td width="6%"></td>
                    <td style={{ color: valueColour }}>
                      {investment.variation.toFixed(2)}
                    </td>
                    <td style={{ color: valueColour }}>
                      {investment.daily_change.toFixed(2)}
                    </td>
                    <td style={{ color: valueColour }}>
                      {investment.daily_change_percent.toFixed(2)}
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
          <tr>
            <td>
              {isOpen && (
                <div className="investment_summary">
                  {/* The chart showing the price/volume history */}
                  <div className="chart">
                    <InvestmentCharts investment_history={investment.history} />
                  </div>
                  {/* The panel on the RHS with details of the investment and the buttons */}
                  <div className="summary">
                    <InvestmentSummary investment={investment} />
                  </div>
                </div>
              )}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default InvestmentCard;