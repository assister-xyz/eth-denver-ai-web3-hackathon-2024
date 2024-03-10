const express = require('express');
const axios = require('axios');
const cors = require('cors');
const cheerio = require('cheerio');
const { ethers } = require('ethers');
const app = express();

app.use(cors());
app.use(express.json());

require('dotenv').config();

const STACK_EXCHANGE_API_KEY = process.env.STACK_EXCHANGE_API_KEY;
const contractABI = [
  "function mint(address receiver, uint256 amount)",
];

const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;

const PRIVATE_KEY = process.env.PRIVATE_KEY;

const provider = new ethers.providers.JsonRpcProvider("https://polygon-mumbai.infura.io/v3/1573346842fe4ed68384624e8bf48e82"); // Use the appropriate network
const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

const contract = new ethers.Contract(CONTRACT_ADDRESS, contractABI, wallet);



async function fetchQuestionUpvotes(answer, tag) {
  const questionId = answer.question_id;
  const questionUrl = `https://api.stackexchange.com/2.3/questions/${questionId}?order=desc&sort=activity&site=stackoverflow&filter=withbody`;
  try {
    const response = await axios.get(questionUrl, { params: { key: STACK_EXCHANGE_API_KEY } });
    const questionData = response.data;
    if (questionData.items[0].tags.includes(tag)) {
      return answer.score;
    }
  } catch (error) {
    console.error(error);
    return 0;
  }
  return 0;
}

async function fetchAnswerUpvotesParallel(answers, tag) {
  let totalUpvotes = 0;
  const promises = answers.map(answer => fetchQuestionUpvotes(answer, tag));
  const results = await Promise.all(promises);
  results.forEach(upvotes => {
    totalUpvotes += upvotes;
  });
  return totalUpvotes;
}

async function fetchTotalUpvotes(userId, tag) {
  let page = 1;
  let hasMore = true;
  let totalUpvotes = 0;
  const regex = /^https:\/\/stackoverflow\.com\/users\/(\d+)(\/[-_a-zA-Z0-9]+)?$/;
  const match = userId.match(regex)[1];
  while (hasMore) {
    const url = `https://api.stackexchange.com/2.3/users/${match}/answers?order=desc&sort=activity&site=stackoverflow&page=${page}&pagesize=100`;
    try {
      const response = await axios.get(url, { params: { key: STACK_EXCHANGE_API_KEY } });
      const data = response.data;
      totalUpvotes += await fetchAnswerUpvotesParallel(data.items, tag);
      hasMore = data.has_more;
      page += 1;
    } catch (error) {
      console.error(error);
      break;
    }
  }

  return totalUpvotes;
}

app.post('/verify-stackoverflow', async (req, res) => {
  const { link, code } = req.body;
  if (!link || !code) {
    return res.status(400).json({ error: 'Stack Overflow link and unique code are required' });
  }

  try {
    const response = await axios.get(link);
    if (response.status === 200) {
      const $ = cheerio.load(response.data);
      const aboutSection = $('.js-about-me-content').text();
      const codePresent = aboutSection.includes(`Code: ${code}`);
      return res.json({ valid: codePresent });
    } else {
      return res.status(404).json({ error: 'About section not found' });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Failed to fetch the profile page' });
  }
});

app.post('/total-upvotes', async (req, res) => {
  const { user_id, tag } = req.body;
  if (!user_id || !tag) {
    return res.status(400).json({ error: 'Missing user_id or tag parameter' });
  }
  
  const totalUpvotes = await fetchTotalUpvotes(user_id, tag);
  return res.json({ total_upvotes: totalUpvotes });
});

//
async function mintTokens(receiver, amount) {
  try {
      const tx = await contract.mint(receiver, amount);
      const displayAmount = amount/Math.pow(10, 18);
      await tx.wait();
      console.log(`Successfully minted ${displayAmount} tokens for ${receiver}`);
      return { success: true, message: `Successfully minted ${displayAmount} tokens for ${receiver}`, link: "https://mumbai.polygonscan.com/tx/"+tx["hash"] };
  } catch (error) {
      console.error("Error minting tokens:", error);
      return { success: false, message: "Error minting tokens" };
  }
}

app.post('/get-tokens', async (req, res) => { // add amount 
  const { user_id, signature} = req.body;
  
  if (!user_id || !signature) {
      return res.status(400).json({ error: "User ID, signature are required." });
  }

  try {
      const recoveredAddress = ethers.utils.verifyMessage(user_id, signature);
      const tag = "nearprotocol";
      var amount = (await fetchTotalUpvotes(user_id, tag)).toString();
      if (amount === "0"){
        amount = "1";
      }
      const parsedAmount = ethers.utils.parseUnits(amount, 18);
      const result = await mintTokens(recoveredAddress, parsedAmount);
      
      return res.status(200).json(result);
  } catch (error) {
      console.error(error);
      return res.status(500).json({ error: "Internal server error" });
  }
});



const port  = 3001;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
