import { useState, useEffect } from "react";
import "./index.css";
import axios from "axios";
const data = [
  {
    name: "Megaport",
    symbol: "MP1",
    yesterday_price: 7.71,
    last_price: 7.55,
    variation: -0.16000000000000014,
    variation_percent: -0.020752269779507154,
    daily_change: -0.14,
    daily_change_percent: -1.82,
    units: 200,
    average_cost: 15.193201499999997,
    total_cost: 3038.6402999999996,
    profit: -1524.6402999999996,
    profit_percent: -50.17508324364683,
    history: {
      20241005: { low: 7.29, high: 7.43, close: 7.36, volume: 486527 },
      20241007: { low: 7.38, high: 7.48, close: 7.42, volume: 147390 },
      20241008: { low: 7.4, high: 7.495, close: 7.46, volume: 123449 },
      20241010: { low: 7.45, high: 7.57, close: 7.5, volume: 743350 },
      20241011: { low: 7.45, high: 7.73, close: 7.58, volume: 921185 },
      20241013: { low: 7.45, high: 7.73, close: 7.58, volume: 921185 },
      20241014: { low: 7.41, high: 7.7, close: 7.44, volume: 672998 },
      20241015: { low: 7.5, high: 7.74, close: 7.71, volume: 989909 },
      20241016: { low: 7.57, high: 7.82, close: 7.57, volume: 303854 },
    },
  },
  {
    name: "Lithium Australia Ltd",
    symbol: "LIT",
    yesterday_price: 0.022,
    last_price: 0.021,
    variation: -0.0009999999999999974,
    variation_percent: -0.04545454545454534,
    daily_change: -0.001,
    daily_change_percent: -4.55,
    units: 15904,
    average_cost: 0.1225,
    total_cost: 1948.24,
    profit: -1598.352,
    profit_percent: -82.04081632653062,
    history: {
      20241005: { low: 0.021, high: 0.0215, close: 0.021, volume: 985527 },
      20241007: { low: 0.021, high: 0.022, close: 0.021, volume: 92257 },
      20241008: { low: 0.021, high: 0.022, close: 0.021, volume: 66100 },
      20241010: { low: 0.021, high: 0.022, close: 0.021, volume: 795817 },
      20241011: { low: 0.021, high: 0.022, close: 0.022, volume: 1040080 },
      20241013: { low: 0.021, high: 0.022, close: 0.022, volume: 1040080 },
      20241014: { low: 0.021, high: 0.022, close: 0.021, volume: 734201 },
      20241015: { low: 0.021, high: 0.026, close: 0.022, volume: 17820235 },
      20241016: { low: 0.022, high: 0.022, close: 0.022, volume: 108018 },
    },
  },
];
function Header() {
  return (
    <>
      <div className="right">
        <span>Admin</span>
        <span>New Investment</span>
        <span>Reports</span>
        <span>Sort</span>
      </div>
    </>
  );
}

function InvestmentCards({ allInvestments }) {
  return (
    <ul>
      {data.map((investment) => (
        <InvestmentCard investment={investment} />
      ))}
    </ul>
  );
}

function InvestmentCard({ investment }) {
  const [isOpen, setIsOpen] = useState(true);
  // return <li>{item.variation_percent}</li>;
  return (
    <>
      <button onClick={() => setIsOpen((open) => !open)}>X</button>
      <span>
        <span>{investment.name}</span>
        <span>{investment.symbol}</span>
        <span>
          <span>Last Price</span>
          <span>+/-</span>
          <span>%</span>
          <span>Daily Gain</span>
          <span>P&L</span>
          <span>%</span>
        </span>
        <div>
          {isOpen && (
            <span>
              <span>{investment.last_price}</span>
              <span>{investment.variation}</span>
              <span>{investment.variation_percent}</span>
              <span>{investment.daily_change}</span>
              <span>{investment.daily_change_percent}</span>
            </span>
          )}
        </div>
      </span>
    </>
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

  // axios({
  //   method: "GET",
  //   url: "http://192.167.1.111/all",
  // })
  //   .then((response) => {
  //     const data = response.data;
  //     console.log(data);
  //   })
  //   .catch((error) => {
  //     if (error.response) {
  //       console.log(error.response);
  //       console.log(error.response.status);
  //       console.log(error.response.headers);
  //     }
  //   });

  // // fetch("https://jsonplaceholder.typicode.com/todos/1")
  // fetch("http://192.167.1.111/all")
  //   .then((response) => response.data.json())
  //   .then((json) => console.log(json));

  useEffect(() => {
    axios
      .get("http://192.167.1.111/all")
      .then((response) => response.data)
      .then((data) => {
        console.log("json", data);
        // setAllInvestments(json.data.movies);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  // useEffect(() => {
  //   axios
  //     .get("http://192.168.1.111/all")
  //     .then((data) => console.log(data.data))
  //     .catch((error) => console.log("----------------", error));
  // });

  return (
    <>
      <Header />
      {/* <InvestmentCards allInvestments={{ data }} /> */}
      <TotalsCard />
      <Footer />
    </>
  );
}
