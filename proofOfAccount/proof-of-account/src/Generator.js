const generatedStrings = new Set();

function generateUniqueRandomString(length = 32) {
  const characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  while (true) {
    let randomString = '';
    for (let i = 0; i < length; i++) {
      randomString += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    if (!generatedStrings.has(randomString)) {
      generatedStrings.add(randomString);
      return randomString;
    }
  }
}

console.log(generateUniqueRandomString());
