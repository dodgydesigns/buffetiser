import React, { PureComponent } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p className="tooltip-desc" style={{ color: `${payload[0].color}` }}>
          ${payload[0].value}
        </p>
        <p className="tooltip-desc" style={{ color: `${payload[1].color}` }}>
          ${payload[1].value}
        </p>
        <p className="tooltip-desc" style={{ color: `${payload[2].color}` }}>
          ${payload[2].value}
        </p>
      </div>
    );
  }

  return null;
};

export default class InvestmentSummary extends PureComponent {
  render() {
    // console.log(this.props.investment_history);
    return (
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={this.props.investment_history}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#ffffff"
            fill="#1b262c"
          />
          <XAxis
            dataKey="date"
            stroke="#ffffff"
            // tickFormatter={(tickItem) => tickItem.format("MMM Do YY")}
            tickCount="5"
          />
          <YAxis stroke="#ffffff" domain={["dataMin", "auto"]} />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line
            type="monotone"
            dataKey="low"
            stroke="#ff3333"
            activeDot={{ r: 8 }}
          />
          <Line
            type="monotone"
            dataKey="high"
            stroke="#82ca9d"
            activeDot={{ r: 8 }}
          />
          <Line
            type="monotone"
            dataKey="close"
            stroke="#f5e642"
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    );
  }
}
