import { useState, React } from "react";
import "../../index.css";

function PopupModal({ props, endpoint, onClose }) {
  const [symbol, setSymbol] = useState(props?.value ?? "");
  const [name, setName] = useState(props?.value ?? "");

  const HandleClose = () => {
    onClose(false);
  };

  return (
    <div className="popup-overlay">
      <div className="popup-modal">
        <h2 className="popup-heading">New Investment Purchase</h2>
        <p>
          If you need to add a new investment to your portfolio, use this
          dialog. It will incorporate a new investment and purchase (of 0) and
          add to the investment list.
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
