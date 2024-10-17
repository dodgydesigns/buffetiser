import { useState, useEffect } from "react";
import "./index.css";
import axios from "axios";

function Header() {
  return (
    <div className="right">
      <span>Admin</span>
      <span>New Investment</span>
      <span>Reports</span>
      <span>Sort</span>
      <button
        onClick={() => {
          axios.post("http://127.0.0.1:8000/update_daily/");
        }}
      >
        Update Daily
      </button>
      <button
        onClick={() => {
          axios.post("http://127.0.0.1:8000/update_all/");
        }}
      >
        Update All
      </button>
    </div>
  );
}

function UpdateData(url) {
  useEffect(() => {
    axios
      .get(url)
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error.response.status);
        console.log(error.response.headers);
        console.log(error.response);
      });
  });
}

function InvestmentCards({ allInvestments }) {
  return allInvestments.map((item) => InvestmentCard(item));
}

function InvestmentCard(investment) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div key={investment.symbol}>
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
