import { useEffect, useState } from "react";

const Navbar = () => {
    const [account, setAccount] = useState("");
  
    useEffect(() => {
      (async () => {
        // Get the active account
        setAccount("");
      })();
    }, []);
  
    // Complete onConnectWallet function
    const onConnectWallet = async () => {};
  
    return (
      <div className="navbar navbar-dark bg-dark fixed-top">
        <div className="container py-2">
          <a href="/" className="navbar-brand">
            Tezos Lottery
          </a>
          <div className="d-flex">
            {/* Call connectWallet function onClick  */}
            <button className="btn btn-outline-info">
              {/* Show account address if wallet is connected */}
              Connect Wallet
            </button>
          </div>
        </div>
      </div>
    );
  };
  
  export default Navbar;
  
  

