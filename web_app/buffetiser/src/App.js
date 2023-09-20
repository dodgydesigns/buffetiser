import React, { useState } from "react"
import Header from "./components/dashboard/Header"
import InvestmentPanel from "./components/investment/Investment_panel"
import InvestmentList from "./components/dashboard/InvestmentList"
import PurchaseData from "./default_data/PurchaseData"

function App() {
    const [purchase, setPurchase] = useState(PurchaseData)
    
  return (
    <>
    <Header text = "Buffetiser Header"/>
    <InvestmentPanel />
    </>
  )
}

export default App