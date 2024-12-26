import { useState, React } from "react";
import "../../index.css";
import "./popup_styles.css";

function PurchaseModal({ investment, constants, endpoint, onClose }) {
  const [symbol] = useState(investment.symbol);
  const [name] = useState(investment.name);
  const [currency, setCurrency] = useState();
  const [exchange, setExchange] = useState();
  const [platform, setPlatform] = useState();
  const [units, setUnits] = useState();
  const [pricePerUnit, setPricePerUnit] = useState();
  const [fee, setFee] = useState();

  const HandleClose = (ok, isOpen) => {
    if (isOpen === "ok") {
    }
    onClose(false);
  };

  return (
    <div className="popup_overlay">
      <div className="popup_modal purchase_modal">
        <h2 className="popup_heading">New Purchase</h2>
        <p>
          If you've purchased shares in an existing investment, use this dialog
          to add the details of the purchase to your portfolio.
        </p>
        <table className="popup_modal_table">
          <tbody>
            <tr>
              <td className="popup_modal_table_label">Symbol</td>
              <td className="popup_modal_table_input">
                <label
                  className="popup_modal_table_text"
                  id={symbol}
                >{symbol}</label>
              </td>
            </tr>
            <tr>
              <td className="popup_modal_table_label">Name</td>
              <td className="popup_modal_table_input">
                <label
                  className="popup_modal_table_text"
                >{name}</label>
              </td>
            </tr>
            <tr>
              <td className="popup_modal_table_label">Currency</td>
              <td className="popup_modal_table_input">
                <select
                  className="popup_modal_table_text"
                  onChange={(e) => setCurrency(e.target.value)}
                >
                  <option>Select...</option>
                  {constants["currency"].map((x) => (
                    <option key={x[0]}>{x[0]}</option>
                  ))}
                </select>
              </td>
            </tr>
            <tr>
              <td className="popup_modal_table_label">Exchange</td>
              <td className="popup_modal_table_input">
                <select
                  className="popup_modal_table_text"
                  defaultValue={0}
                  onChange={(e) => setExchange(e.target.value)}
                >
                  <option>Select...</option>
                  {constants["exchange"].map((x) => (
                    <option key={x[0]}>{x[0]}</option>
                  ))}
                </select>
              </td>
            </tr>
            <tr>
              <td className="popup_modal_table_label">Platform</td>
              <td className="popup_modal_table_input">
                <select
                  className="popup_modal_table_text"
                  defaultValue={0}
                  onChange={(e) => setPlatform(e.target.value)}
                >
                  <option>Select...</option>
                  {constants["platform"].map((x) => (
                    <option key={x[0]}>{x[0]}</option>
                  ))}
                </select>
              </td>
            </tr>
            <tr>
              <td className="popup_modal_table_label">Units</td>
              <td className="popup_modal_table_input">
                <input
                  style={{ width: "4rem" }}
                  className="popup_modal_table_text"
                  type="number"
                  onChange={(e) => setUnits(e.target.value)}
                ></input>
                <span style={{ paddingLeft: "1rem" }}>0 to watch</span>
              </td>
            </tr>
            <tr>
              <td className="popup_modal_table_label">Price/Unit $AU</td>
              <td className="popup_modal_table_input">
                <input
                  style={{ width: "4rem" }}
                  className="popup_modal_table_text"
                  type="number"
                  onChange={(e) => setPricePerUnit(e.target.value)}
                ></input>
              </td>
            </tr>
            <tr>
              <td className="popup_modal_table_label">Fee $AU</td>
              <td className="popup_modal_table_input">
                <input
                  style={{ width: "4rem" }}
                  className="popup_modal_table_text"
                  type="number"
                  onChange={(e) => setFee(e.target.value)}
                ></input>
              </td>
            </tr>
          </tbody>
        </table>
        <div>
        <div
          className="new_purchase_cancel"
          style={{ marginRight: "3rem" }}
          onClick={(e) => {
            e.stopPropagation();
            HandleClose("cancel", false);
          }}
        >
          Cancel
        </div>
        <div
          className="new_purchase_save"
          onClick={(e) => {
            e.stopPropagation();
            // HandleClose("ok", false);

            const result = {
              symbol: symbol,
              currency: currency,
              exchange: exchange,
              platform: platform,
              units: units,
              pricePerUnit: pricePerUnit,
              fee: fee,
            };

            fetch("127.0.0.1/purchase/", {
              method: "POST",
              headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
              },
              body: JSON.stringify(result),
            });
            console.log(JSON.stringify(result));
          }}
        >
          Save
        </div>
        </div>
      </div>
    </div>
  );
}

export default PurchaseModal;
