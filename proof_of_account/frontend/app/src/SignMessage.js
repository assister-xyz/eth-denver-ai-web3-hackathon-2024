import React, { useState } from 'react';
import { ethers } from 'ethers';

const SignMessage = ({ initialMessage }) => {
  const message = initialMessage;
  const [signedMessage, setSignedMessage] = useState('');

  // Function to request account access and sign the message
  const signMessage = async () => {
    try {
      if (!window.ethereum) throw new Error('No crypto wallet found. Please install it.');

      // Request account access if needed
      await window.ethereum.request({ method: 'eth_requestAccounts' });

      // We create a new provider connected to the wallet
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = provider.getSigner();

      // Sign the message
      const signature = await signer.signMessage(message);
      setSignedMessage(signature);

      console.log('Signed Message:', signature);
    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <div style={styles.container}>
      <button style={styles.button} onClick={signMessage}>Sign Message</button>
      {signedMessage && (
        <p style={styles.message}>Signed Message: {signedMessage}</p>
      )}
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '10vh',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    cursor: 'pointer',
  },
  message: {
    marginTop: '20px',
    fontSize: '18px',
    fontWeight: 'bold',
    textAlign: 'center',
  },
};

export default SignMessage;
