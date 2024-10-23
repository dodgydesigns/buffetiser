import { useState, useEffect } from "react";
import axios from "axios";
import InvestmentSummary from "./components/chart/investment_summary";
import "./index.css";

const baseURL = "127.0.0.1:8000";

function Header() {
  return (
    <div className="header">
      <span
        className="header_bar_div"
        onClick={() => {
          axios.request(baseURL + "/config/");
        }}
      >
        Configuration
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          axios.post(baseURL + "/new_investment/");
        }}
      >
        New Investment
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          axios.post(baseURL + "/reports/");
        }}
      >
        Reports
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          axios.post(baseURL + "/help/");
        }}
      >
        Help
      </span>
    </div>
  );
}

function InvestmentCards({ allInvestments }) {
  return allInvestments.map((item) => InvestmentCard(item));
}

function InvestmentCard(investment) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div key={investment.symbol}>
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
                    <td
                      style={
                        investment.variation < 0
                          ? { color: "#ff9999" }
                          : { color: "#55ff55" }
                      }
                    >
                      {investment.variation.toFixed(2)}
                    </td>
                    <td
                      style={
                        investment.variation < 0
                          ? { color: "#ff9999" }
                          : { color: "#55ff55" }
                      }
                    >
                      {investment.variation_percent.toFixed(2)}%
                    </td>
                    <td width="6%"></td>
                    <td
                      style={
                        investment.variation < 0
                          ? { color: "#ff9999" }
                          : { color: "#55ff55" }
                      }
                    >
                      {investment.variation.toFixed(2)}
                    </td>
                    <td
                      style={
                        investment.variation < 0
                          ? { color: "#ff9999" }
                          : { color: "#55ff55" }
                      }
                    >
                      {investment.daily_change.toFixed(2)}
                    </td>
                    <td
                      style={
                        investment.variation < 0
                          ? { color: "#ff9999" }
                          : { color: "#55ff55" }
                      }
                    >
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
                <div className="chart">
                  <InvestmentSummary investment_history={investment.history} />
                </div>
              )}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

function TotalsCard() {
  return <></>;
}

function Footer() {
  return <></>;
}

export default function App() {
  const [allInvestments, setAllInvestments] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/all")
      .then((response) => {
        setAllInvestments(response.data.all_investment_data);
      })
      .catch((error) => {
        console.log(error.response.status);
        console.log(error.response.headers);
        console.log(error.response);
      });
  }, []);

  return (
    <>
      <Header />
      <InvestmentCards allInvestments={allInvestments} />
      <TotalsCard />
      <Footer />
    </>
  );
}
