import React, {useEffect} from 'react';
import './App.css';
import StackOverflowLinkVerifier from './StackOverflowLinkVerifier';

function App() {
  useEffect(() => {
    document.title = "UVR";
  }, []);
  return (
    <div className="App">
      <h1>Stack Overflow Up Vote Reward</h1>
      <StackOverflowLinkVerifier />  
    </div>
  );
}

export default App;