import React, { useState } from 'react';
import Contributor from 'E:\javaProjects\eth-denver-ai-web3-hackathon-2024\proofOfAccount\proof-of-account\src\Contributor.js';

import { generateUniqueRandomString } from './Generator';
import { checkAboutSection } from './validateProfile';

function isStackOverflowLink(link) {
  return link.startsWith("https://stackoverflow.com/users/");
}

function App() {
  const [generatedCode, setGeneratedCode] = useState(null);
  const [newContributor, setNewContributor] = useState(null);
  const [contributors, setContributors] = useState([]);
  const [stackoverflowLink, setStackoverflowLink] = useState('');

  const handleVerificationCode = () => {
    setGeneratedCode(null);
    const contributor = new Contributor(stackoverflowLink);
    contributor.setUniqueCode(generateUniqueRandomString());
    setNewContributor(contributor);
    setGeneratedCode(contributor.getUniqueCode());
  };

  const handleVerifyProfile = () => {
    if (checkAboutSection(newContributor.stackoverflowAccountLink, generatedCode)) {
      setContributors([...contributors, newContributor]);
      // Implement signing and sending signature to backend for verification
    } else {
      console.error("Verification failed. Please try again.");
    }
  };

  return (
    <div>
      <h1>Register as contributor👤</h1>
      <p>Please provide a link to your Stack Overflow account for verification.</p>
      <input
        type="text"
        value={stackoverflowLink}
        onChange={(e) => setStackoverflowLink(e.target.value)}
        placeholder="Your Stack Overflow Profile Link"
      />
      {stackoverflowLink && isStackOverflowLink(stackoverflowLink) ? (
        <>
          <p>Success! Valid Stack Overflow link.</p>
          <button onClick={handleVerificationCode}>Get Verification Code</button>
          {generatedCode && (
            <div>
              <p>Please, copy and paste this code into your Stack Overflow about section:</p>
              <code>Contributor Code: {generatedCode}</code>
            </div>
          )}
          <button onClick={handleVerifyProfile}>Verify Profile</button>
        </>
      ) : (
        <p>Invalid Stack Overflow account link. Please enter a valid link.</p>
      )}
    </div>
  );
}

export default App;
