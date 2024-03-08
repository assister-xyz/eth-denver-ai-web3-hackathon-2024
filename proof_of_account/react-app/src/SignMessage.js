import React, { useState } from 'react';
import './SignMessage.css';
const { ethers } = require("ethers");

const SignMessage = ({ initialMessage, onSignMessage }) => {
  const message = initialMessage;
  const [signedMessage, setSignedMessage] = useState('');
  const [response, setResponse] = useState(null);

  const signMessage = async () => {
    try {
      if (!window.ethereum) throw new Error('No crypto wallet found. Please install it.');

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
      <button
        className="sign-button"
        onClick={signMessage}>Sign Message and Get Reward
      </button>
      {signedMessage && (
        <p className="signed-message">Signed Message: {signedMessage}</p>
      )}
      {response && (
        <div className="response-container">
          <p className="response-message">{response.message}</p>
          <div class="link1">
          <a href={response.link} target="_blank" rel="noopener noreferrer">View Transaction</a>
          </div>
        </div>
      )}
    </div>
  );
};

export default SignMessage;
