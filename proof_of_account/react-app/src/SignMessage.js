import React, { useState } from 'react';
import './SignMessage.css';
const { ethers } = require("ethers");


const SignMessage = ({ initialMessage, onSignMessage }) => {
  const message = initialMessage;
  const [signedMessage, setSignedMessage] = useState('');
  const [response, setResponse] = useState(null);
  const [tokenAdded, setTokenAdded] = useState(false); 
  const tokenAddress = process.env.REACT_APP_CONTRACT_ADDRESS;
  const tokenSymbol = 'UVR';
  const tokenDecimals = 18;
  const tokenImage = 'https://static.thenounproject.com/png/341245-200.png';

  const AddUVRToken = async () => {
    try {
      if (typeof window.ethereum === 'undefined') {
        throw new Error('MetaMask or other Ethereum wallet provider not detected.');
      }

      const wasAdded = await window.ethereum.request({
        method: 'wallet_watchAsset',
        params: {
          type: 'ERC20',
          options: {
            address: tokenAddress,
            symbol: tokenSymbol,
            decimals: tokenDecimals,
            image: tokenImage,
          },
        },
      });

      if (wasAdded) {
        console.log('Thanks for your interest!');
        setTokenAdded(true); 
      } else {
        console.log('Your loss!');
      }
    } catch (error) {
      console.log(error);
    }
  };

  const signMessage = async () => {
    try {
      if (typeof window.ethereum === 'undefined') {
        throw new Error('No crypto wallet found. Please install it.');
      }

      await window.ethereum.request({ method: 'eth_requestAccounts' });

      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = provider.getSigner();

      const signature = await signer.signMessage(message);
      setSignedMessage(signature);

      console.log('Signed Message:', signature);

      const data = {
        user_id: message,
        signature: signature
      };

      fetch(`${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/get-tokens`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
        .then(response => response.json())
        .then(result => {
          console.log('Response from server:', result);

          setResponse(result);

          onSignMessage(signature);
        })
        .catch(error => {
          console.error('Error:', error.message);
        });

    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <div className="container-1">
      <div className="container-2">
      <button
        className="add-token-button"
        onClick={() => { AddUVRToken(); }}>Add UVR Token
      </button> 
      {tokenAdded && ( 
        <button
          className="sign-button"
          onClick={() => { signMessage(); }}>Sign Message and Get Reward
        </button>
      )}
      </div>
      {/* {signedMessage && (
        <p className="signed-message">Signed Message: {signedMessage}</p>
      )} */}
      {response && (
        <div className="response-container">
          <p className="response-message">{response.message}</p>
          <div className="link1">
            <a href={response.link} target="_blank" rel="noopener noreferrer">View Transaction</a>
          </div>
        </div>
      )}
      
    </div>
  );
};

export default SignMessage;