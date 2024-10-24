import axios from "axios";

const baseURL = "127.0.0.1:8000";

function MenuBar() {
  return (
    <div className="header">
      <span
        className="header_bar_div"
        onClick={() => {
          axios.request(baseURL + "/config/");
        }}
      >
        Configuration
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          axios.post(baseURL + "/new_investment/");
        }}
      >
        New Investment
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          axios.post(baseURL + "/reports/");
        }}
      >
        Reports
      </span>
      <span
        className="header_bar_div"
        onClick={() => {
          axios.post(baseURL + "/help/");
        }}
      >
        Help
      </span>
    </div>
  );
}

export default MenuBar;
