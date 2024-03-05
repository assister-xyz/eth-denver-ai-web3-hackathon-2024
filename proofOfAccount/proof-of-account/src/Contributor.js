class Contributor {
    constructor(stackoverflowAccountLink) {
      this.stackoverflowAccountLink = stackoverflowAccountLink;
      this.uniqueCode = null;
      this.verified = false;
    }
  
    setUniqueCode(uniqueCode) {
      this.uniqueCode = uniqueCode;
    }
  
    getUniqueCode() {
      return this.uniqueCode;
    }
  
    getVerified() {
      return this.verified;
    }
  
    setVerified(verified) {
      this.verified = verified;
    }
  
    toString() {
      return `StackOverflow Account Link: ${this.stackoverflowAccountLink}, Unique Code: ${this.uniqueCode}, Verified: ${this.verified}`;
    }
  }
  