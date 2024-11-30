import React from "react";
import "../../index.css";

function PopupModal({ endpoint, onClose }) {
  const handleClose = (ok, isOpen) => {
    console.log("PopupModal:", ok, endpoint);
    if (isOpen === "ok") {
      console.log("PopupModal:", ok, endpoint);
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
              <td>
                <input type="text"></input>
              </td>
            </tr>
            <tr>
              <td className="popup-modal-table-label">Name</td>
              <td>
                <input type="text"></input>
              </td>
            </tr>
          </tbody>
        </table>
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleClose("cancel", false);
          }}
        >
          Cancel
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleClose("ok", false);
          }}
        >
          Save
        </button>
      </div>
    </div>
  );
}

export default PopupModal;
