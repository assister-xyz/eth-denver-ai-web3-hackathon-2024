const axios = require('axios');
const cheerio = require('cheerio');

async function checkAboutSection(stackoverflowLink, uniqueCode) {
  try {
    const response = await axios.get(stackoverflowLink);
    if (response.status === 200) {
      const $ = cheerio.load(response.data);
      const aboutSection = $('.js-about-me-content').text();
      const regex = new RegExp(`Contributor Code: ${uniqueCode}`);
      const codePresent = regex.test(aboutSection);
      return codePresent;
    } else {
      console.log('Failed to fetch the profile page.');
    }
  } catch (error) {
    console.error('Error fetching profile page:', error);
  }
}