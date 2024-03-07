import React, { useState } from 'react';
import SignMessage from './SignMessage';
import './StackOverflowLinkVerifier.css';

function StackOverflowLinkVerifier() {
  const [link, setLink] = useState('');
  const [isValid, setIsValid] = useState(false);
  const [locked, setLocked] = useState(false);
  const [code, setCode] = useState('');
  const [verificationResult, setVerificationResult] = useState(null);
  const [totalUpvotes, setTotalUpvotes] = useState(null);
  const [signedMessage, setSignedMessage] = useState('');

  const handleSignMessage = (message) => {
    setSignedMessage(message);
  };

  const isStackOverflowLink = (link) => {
    const regex = /^https:\/\/stackoverflow\.com\/users\/(\d+)(\/[-_a-zA-Z0-9]+)?$/;
    const match = link.match(regex);
    if (match) {
      return true;
    }
    return false;
  };

  const handleVerify = () => {
    setIsValid(isStackOverflowLink(link));
  };

  const handleLock = () => {
    setLocked(true);
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < 20; i++) {
      result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    setCode(result);
  };

  const handleUnlock = () => {
    setLocked(false);
    setCode('');
    setVerificationResult(null);
  };

  const handleVerifyStackOverflow = () => {
    const data = {
      link: link,
      code: code
    };

    fetch(`${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/verify-stackoverflow`, { // Using env variable for host
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(result => {
        console.log('Response from server:', result);
        if (result.valid) {
          setVerificationResult('Success');
        } else {
          setVerificationResult('Failed to verify');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setVerificationResult('Failed to verify');
      });
  };

  const handleTotalUpvotes = () => {
    const data = {
      user_id: link,
      tag: 'nearprotocol'
    };

    fetch(`${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/total-upvotes`, { // Using env variable for host
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(result => {
        console.log('Response from server:', result);
        if (result.total_upvotes !== undefined) {
          setTotalUpvotes(result.total_upvotes);
        } else {
          setVerificationResult('Failed to get total upvotes');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setVerificationResult('Failed to get total upvotes');
      });
  };

  return (
    <div className="container">
      <div className="input-container">
        <input
          className="input-field"
          type="text"
          value={link}
          onChange={(e) => setLink(e.target.value)}
          placeholder="Enter Stack Overflow Profile Link"
          disabled={locked}
        />
        <button
          className="verify-button"
          onClick={handleVerify}
          disabled={locked}
        >
          Verify Link
        </button>
        <br />
        {isValid ? (
          <p className="valid-message">Valid Stack Overflow Profile Link</p>
        ) : (
          <p className="invalid-message">Invalid Stack Overflow Profile Link</p>
        )}
        {isValid && !locked && (
          <div>
            <button
              className="lock-button"
              onClick={handleLock}
            >
              Lock
            </button>
          </div>
        )}
      </div>

      {locked && (
        <div className="locked-container">
          <div className="code-container">
            <code className="code">Code: {code}</code>
            <button
              className="unlock-button"
              onClick={handleUnlock}
            >
              Unlock
            </button>
            <button
              className="verify-code-button"
              onClick={handleVerifyStackOverflow}
            >
              Verify Code
            </button>
            <button
              className="upvote-button"
              onClick={handleTotalUpvotes}
            >
              Total Upvotes
            </button>
            {totalUpvotes !== null && (
              <p className="total-upvotes">Total Upvotes: {totalUpvotes}</p>
            )}
            {verificationResult !== null && (
              <>
                <p className="verification-result">
                  {verificationResult === 'Success' ? 'Success' : 'Failed to verify'}
                </p>
                {verificationResult === 'Success' && <div>
                  <SignMessage initialMessage={link} onSignMessage={handleSignMessage} />
                </div>}
                
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default StackOverflowLinkVerifier;
