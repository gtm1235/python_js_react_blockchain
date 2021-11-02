import React, { useState, useEffect } from "react";
import logo from '../assets/logo.png';
import { API_BASE_URL} from '../config';
import { Link } from 'react-router-dom';
// import Blockchain from './Blockchain';
// import ConductTransaction from "./conductTransaction";

function App() {
  const [walletInfo, setWalletInfo] = useState({});

  useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/info`)
      .then(response => response.json())
      .then(json => setWalletInfo(json));
  }, []);

  const { address, balance} = walletInfo

  return (
    <div className="App">
      <img className="logo" src={logo} alt="application logo" />
      <h3>Welcome to Pychain</h3>
      <br />
      
      <Link to="/blockchain">Blockchain</Link>
      <Link to="/conduct-transaction">Conduct a Transaction</Link>
      <Link to="/transaction-pool">Transaction Pool</Link>

      <div className="WalletInfo">
        <hr />
        <div>Address: {address}</div>
        <div>Balance: {balance}</div>
      </div>
      <br />
      {/* <Blockchain />
      <br />
      <ConductTransaction /> */}
    </div>
  );
}


export default App;
