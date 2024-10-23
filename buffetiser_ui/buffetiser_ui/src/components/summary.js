import React, { PureComponent } from "react";

export default class InvestmentSummary extends PureComponent {
  render() {
    const data = this.props.investment;
    return (
      <>
        <table>
          <tbody>
            <tr>
              <td>Units</td>
              <td>{data.units}</td>
            </tr>
            <tr>
              <td>Average Cost</td>
              <td>${data.average_cost.toFixed(2)}</td>
            </tr>
            <tr>
              <td>Total Cost</td>
              <td>${data.total_cost.toFixed(2)}</td>
            </tr>
            <tr>
              <td>Profit</td>
              <td
                style={
                  data.profit < 0 ? { color: "#ff9999" } : { color: "#55ff55" }
                }
              >
                ${data.profit.toFixed(2)}
              </td>
              <td
                style={
                  data.profit_percent < 0
                    ? { color: "#ff9999" }
                    : { color: "#55ff55" }
                }
              >
                {data.profit_percent.toFixed(2)}%
              </td>
            </tr>
          </tbody>
        </table>
        <div className="summary_buttons">
          <button>Buy</button>
          <button>Sell</button>
          <button style={{ backgroundColor: "#ff2222" }}>Remove</button>
        </div>
      </>
    );
  }
}
