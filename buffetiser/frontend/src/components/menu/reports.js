import React, { useEffect, useState } from "react";
import axios from "axios";
import "./reports.css";

const baseURL = "http://127.0.0.1:8000";

const InvestmentTransactions = () => {
  const [investments, setInvestments] = useState([]);
  const [loading, setLoading] = useState(true);

  function getDate(transaction) {
    return transaction.date || transaction.reinvestment_date || transaction.payment_date;
  }

  function getTransactionType(transaction) {
    return String(transaction.type).charAt(0).toUpperCase() + String(transaction.type).slice(1);
  }

  function getUnits(transaction) {
    return transaction.units !== undefined ? transaction.units : "-";
  }

  function getFee(transaction) {
    return transaction.fee !== undefined ? transaction.fee : "-";
  }

  function getPrice(transaction) {
    if (transaction.price_per_unit) {
      return transaction.price_per_unit.toFixed(2);
    } else if (transaction.value) {
      return transaction.value.toFixed(2);
    }
    return "-";
  }

  useEffect(() => {
    axios.get(baseURL + "/reports/")
      .then((response) => {
        const data = response.data;
        const values = Object.values(data); // Convert object to array
        setInvestments(values);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading transactions...</p>;

  return (
    <>
        <div>
            <button className="cancel-button" onClick={() => window.history.back()}>Cancel</button>
            <button className="print-button" onClick={() => window.print()}>Print</button>
        </div>
        <div className="reports">
        <h1>Investment Transactions</h1>
        {investments.map((investment, index) => (
            <div key={`investment-${index}`}>
            <h3>({investment.symbol}) {investment.name}</h3>
            <table>
                <thead>
                <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Units</th>
                    <th>Price</th>
                    <th>Fee</th>
                </tr>
                </thead>
                <tbody>
                {investment.transactions.map((transaction, tIndex) => (
                    <tr key={`transaction-${index}-${tIndex}`}>
                    <td>{getDate(transaction)}</td>
                    <td>{getTransactionType(transaction)}</td>
                    <td>{getUnits(transaction)}</td>
                    <td>{getPrice(transaction)}</td>
                    <td>{getFee(transaction)}</td>
                    </tr>
                ))}
                </tbody>
            </table>
            </div>
        ))}
        </div>
    </>
  );
};

export default InvestmentTransactions;
