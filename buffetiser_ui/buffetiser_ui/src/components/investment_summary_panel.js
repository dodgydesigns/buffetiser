import React, { PureComponent } from "react";

/* 
Provides a panel to the right of the investment price/volume chart that shows
specific information about an Investment:
 - Total units held
 - Average cost over all purchases
 - Total cost of all purchases
 - Profit info

Does not include profit/loss due to sales. (maybe it should???)
*/
import "../index.css";

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
              <td>Average</td>
              <td>${data.average_cost.toFixed(2)}</td>
            </tr>
            <tr>
              <td>Total</td>
              <td>${data.total_cost.toFixed(2)}</td>
            </tr>
            <tr>
              <td>Value</td>
              <td>${(data.units * data.last_price).toFixed(2)}</td>
            </tr>
            <tr>
              <td>Profit</td>
              <td
                style={
                  data.profit < 0 ? { color: "#ff4444" } : { color: "#82ca9d" }
                }
              >
                {data.profit > 0
                  ? "$" + data.profit.toFixed(2)
                  : "-$" + data.profit.toFixed(2).replace("-", "")}
              </td>
              <td
                style={
                  data.profit_percent < 0
                    ? { color: "#ff4444" }
                    : { color: "#82ca9d" }
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
        </div>
        <button className="remove">Remove</button>
      </>
    );
  }
}
