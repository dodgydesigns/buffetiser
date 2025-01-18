import { useState, React } from "react";
import DatePicker from "react-datepicker";
import { registerLocale } from  "react-datepicker";
import { enAU } from 'date-fns/locale/en-AU';

import "../menu/popup_styles.css";
import "react-datepicker/dist/react-datepicker.css";

registerLocale('enAU', enAU)

function RemoveModal({ investment, constants, endpoint, onClose }) {
  const [symbol] = useState(investment.symbol);
  const [name] = useState(investment.name);
  const endpoint_string = endpoint;

  const HandleClose = (button) => {
    if (button === "ok") {
    }
    onClose(false);
  };

  return (
    <div className="popup_overlay">
      <div className="popup_modal sale_modal">
        <h2 className="popup_heading">Remove Investment</h2>
        <div>
          Are you absolutely sure you want to remove <p style={{color: "red"}}>{name} ({symbol})</p> from Buffetiser?
        </div>
        <p>
          This action CAN NOT be undone. All history associate with {symbol} will be lost.
        </p>
        <div>
          <div
            className="save"
            onClick={(e) => {
              e.stopPropagation();
              // HandleClose("ok", false);

              const result = {
                symbol: symbol,
              };
              fetch(endpoint_string, {
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
          REMOVE
        </div>
        <div
            className="cancel"
            style={{ marginRight: "3rem" }}
            onClick={(e) => {
              e.stopPropagation();
              HandleClose("cancel", false);
            }}
          >
            Cancel
        </div>
      </div>
    </div>
  </div>);
}

export default RemoveModal;
