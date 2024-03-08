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
    return regex.test(link);
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setLink(value);
    setIsValid(isStackOverflowLink(value));
  };

  const handleLock = () => {
    if (isValid) {
      setLocked(true);
      const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let result = '';
      for (let i = 0; i < 20; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
      }
      setCode(result);
    }
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

    fetch(`${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/verify-stackoverflow`, {
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

    fetch(`${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/total-upvotes`, {
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
      className={`input-field ${isValid ? 'shrink' : ''}`} // Dummy
      type="text"
      value={link}
      onChange={handleInputChange}
      placeholder="Enter Stack Overflow Profile Link To Register"
      disabled={locked}
    />
      {isValid && !locked && (
        <button
          className="lock-button"
          onClick={handleLock}
        >
          Lock
        </button>
      )}
      {locked && (
        <button
          className="lock-button"
          disabled
        >
          Locked
        </button>
      )}
    </div>

      {locked && (
         <div className="locked-container">
         <div className="code-container">
           <p className="about-text">
             Please add the following text to your about section on your Stack Overflow account
           </p>
           <div class="code-background">
            <code className="code">Code: {code}</code>
           </div>
           <button className="unlock-button" onClick={handleUnlock}>
             Unlock
           </button>
           <button className="verify-code-button" onClick={handleVerifyStackOverflow}>
             Verify Code
           </button>
           <button className="upvote-button" onClick={handleTotalUpvotes}>
             Total Upvotes
           </button>
           {totalUpvotes !== null && (
            <div class="upvotes-background">
             <p className="total-upvotes">Total Upvotes: {totalUpvotes}</p>
            </div>
           )}
           {verificationResult !== null && (
             <>
             <div class="verification-background"> 
               <p className={verificationResult === 'Success' ? 'success' : 'verification-result'}>
                 {verificationResult === 'Success' ? 'Success' : 'Failed to verify'}
               </p>
              </div>
               {verificationResult === 'Success' && (
                 <div>
                   <SignMessage initialMessage={link} onSignMessage={handleSignMessage} />
                 </div>
               )}
             </>
           )}
         </div>
       </div>
      )}
    </div>
  );
}

export default StackOverflowLinkVerifier;
