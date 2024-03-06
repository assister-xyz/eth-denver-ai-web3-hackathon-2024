import React, { useState } from 'react';
import SignMessage from './SignMessage';
import './styles.css'; // Import the styles

function StackOverflowLinkVerifier() {
  const [link, setLink] = useState('');
  const [userId, setUserId] = useState(null);
  const [isValid, setIsValid] = useState(false);
  const [locked, setLocked] = useState(false);
  const [code, setCode] = useState('');
  const [verificationResult, setVerificationResult] = useState(null);
  const [totalUpvotes, setTotalUpvotes] = useState(null); // Added state for total upvotes
  const isStackOverflowLink = (link) => {
    const regex = /^https:\/\/stackoverflow\.com\/users\/(\d+)(\/[-_a-zA-Z0-9]+)?$/;
    const match = link.match(regex);
    if (match) {
      const extractedUserId = match[1]; // Extract user ID
      setUserId(extractedUserId); // Set user ID state
      return true;
    }
    return false;
  };

  const handleVerify = () => {
    setIsValid(isStackOverflowLink(link));
  };

  const handleLock = () => {
    setLocked(true);
    // Generate a unique random character sequence with length 20
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
    // Prepare data to send in the POST request
    const data = {
      link: link,
      code: code
    };

    fetch('http://127.0.0.1:5000/verify-stackoverflow', {
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
    // Prepare data to send in the POST request
    const data = {
      user_id: userId, // Use extracted user ID
      tag: 'nearprotocol' // Example tag
    };

    fetch('http://127.0.0.1:5000/total-upvotes', {
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
      {userId && (
        <p>User ID: {userId}</p>
      )}
      {locked && (
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


        
        {verificationResult !== null && (
          <>
            <p className="verification-result">
              {verificationResult === 'Success' ? 'Success' : 'Failed to verify'}
            </p>
            {verificationResult === 'Success' && <SignMessage initialMessage={link}/>}
          </>
        )}
        {totalUpvotes !== null && (
            <p className="total-upvotes">Total Upvotes: {totalUpvotes}</p>
          )}
      </div>
      )}
    </div>
  );
}

export default StackOverflowLinkVerifier;


