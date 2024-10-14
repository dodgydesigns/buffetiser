import { useState, useEffect } from "react";
import "./index.css";
import axios from "axios";

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

function InvestmentCard({ allInvestments }) {
  const [isOpen, setIsOpen] = useState(true);
  return (
    <>
      <p>{allInvestments}</p>
      <button onClick={() => setIsOpen((open) => !open)}>X</button>
      <span>
        <span>MegaPort Ltd</span>
        <span>(ASX:MP1)</span>
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
              <span>12.1</span>
              <span>+5.1</span>
              <span>+1.2%</span>
              <span>12.1</span>
              <span>+5.1</span>
              <span>+1.2%</span>
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

  useEffect(() => {
    axios.get("/api/getEmployeeList").then((res) => {
      setAllInvestments(res.data);
    });
  });

  return (
    <>
      <Header />
      <InvestmentCard allInvestments={{ allInvestments }} />
      <TotalsCard />
      <Footer />
    </>
  );
}
