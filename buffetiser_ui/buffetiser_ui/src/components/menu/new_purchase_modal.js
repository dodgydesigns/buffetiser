import { useState, React } from "react";
import axios from "axios";
import "../../index.css";

function PopupModal({ props, endpoint, onClose }) {
  const [symbol, setSymbol] = useState(props?.value ?? "");
  const [name, setName] = useState(props?.value ?? "");
  const [currency, setCurrency] = useState(props?.value ?? "");
  const [exchange, setExchange] = useState(props?.value ?? "");
  const [platform, setPlatform] = useState(props?.value ?? "");
  const [units, setUnits] = useState(props?.value ?? "");
  const [pricePerUnit, setPricePerUnit] = useState(props?.value ?? "");
  const [fee, setFee] = useState(props?.value ?? "");

  const constants = props["constants"];
  const HandleClose = (ok, isOpen) => {
    if (isOpen === "ok") {
    }
    onClose(false);
  };

  return (
    <div className="popup-overlay">
      <div className="popup-modal">
        <h2 className="popup-heading">New Investment Purchase</h2>
        <p>
          If you need to add a new investment to your portfolio, use this
          dialog. It will incorporate a new investment and purchase and add to
          the investment list.
        </p>
        <table className="popup-modal-table">
          <tbody>
            <tr>
              <td className="popup-modal-table-label">Symbol</td>
              <td className="popup-modal-table-input">
                <input
                  className="popup-modal-table-text"
                  id={symbol}
                  onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                />
              </td>
            </tr>
            <tr>
              <td className="popup-modal-table-label">Name</td>
              <td className="popup-modal-table-input">
                <input
                  className="popup-modal-table-text"
                  id={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </td>
            </tr>
            <tr>
              <td className="popup-modal-table-label">Currency</td>
              <td className="popup-modal-table-input">
                <select
                  className="popup-modal-table-text"
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
              <td className="popup-modal-table-label">Exchange</td>
              <td className="popup-modal-table-input">
                <select
                  className="popup-modal-table-text"
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
              <td className="popup-modal-table-label">Platform</td>
              <td className="popup-modal-table-input">
                <select
                  className="popup-modal-table-text"
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
              <td className="popup-modal-table-label">Units</td>
              <td className="popup-modal-table-input">
                <input
                  style={{ width: "4rem" }}
                  className="popup-modal-table-text"
                  type="number"
                  onChange={(e) => setUnits(e.target.value)}
                ></input>
                <span style={{ paddingLeft: "1rem" }}>0 to watch</span>
              </td>
            </tr>
            <tr>
              <td className="popup-modal-table-label">Price/Unit $AU</td>
              <td className="popup-modal-table-input">
                <input
                  style={{ width: "4rem" }}
                  className="popup-modal-table-text"
                  type="number"
                  onChange={(e) => setPricePerUnit(e.target.value)}
                ></input>
              </td>
            </tr>
            <tr>
              <td className="popup-modal-table-label">Fee $AU</td>
              <td className="popup-modal-table-input">
                <input
                  style={{ width: "4rem" }}
                  className="popup-modal-table-text"
                  type="number"
                  onChange={(e) => setFee(e.target.value)}
                ></input>
              </td>
            </tr>
            <tr>
              <td>
                <button
                  className="popup_button"
                  style={{ marginRight: "3rem" }}
                  onClick={(e) => {
                    e.stopPropagation();
                    HandleClose("cancel", false);
                  }}
                >
                  Cancel
                </button>
              </td>
              <td>
                <button
                  className="popup_button"
                  onClick={(e) => {
                    e.stopPropagation();
                    HandleClose("ok", false);

                    const result = {
                      symbol: symbol,
                      name: name,
                      currency: currency,
                      exchange: exchange,
                      platform: platform,
                      units: units,
                      pricePerUnit: pricePerUnit,
                      fee: fee,
                    };
                    fetch(endpoint, {
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
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PopupModal;
