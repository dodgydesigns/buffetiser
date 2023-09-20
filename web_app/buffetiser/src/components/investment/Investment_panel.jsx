import React, { useState } from "react"

function InvestmentPanel() {//symbol, investment_name, units, price_per_unit, fee) {
  /* Add private to this */
  const [symbol, setSymbol] = useState("ASX")
  const [investment_name, setInvestmentName] = useState("Aust.. Securities Exchange")
  const [units, setUnits] = useState(10)
  const [price_per_unit, setPricePerUnit] = useState(1.00)
  const [fee, setFee] = useState(11.0)

  return (
    <>
      <table>
        <tr>
          <th>symbol</th>
          <th>investment_name</th> 
          <th>units</th>
          <th>price_per_unit</th>
          <td>fee</td>
        </tr>
        <tr>
          <td>{symbol}</td>
          <td>{investment_name}</td>
          <td>{units}</td>
          <td>{price_per_unit}</td>
          <td>{fee}</td>
        </tr>
      </table>
    </>
  )
  }

export default InvestmentPanel