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
import "../index.css";

export default class InvestmentCharts extends PureComponent {
  render() {
    return (
      <ResponsiveContainer width="98%" height={300}>
        <LineChart
          data={this.props.portfolio_history}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#0f4c75"
            fill="#1b262c"
          />
          <XAxis
            dataKey="date"
            stroke="#ffffff"
            fontSize="10"
            padding={{ left: 20, right: 30 }}
          />
          <YAxis
            yAxisId="left"
            stroke="#ffffff"
            fontSize="10"
            domain={["dataMin", "auto"]}
          />
          <Tooltip />
          <Legend />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="total"
            stroke="#f5e642"
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    );
  }
}
