from web3 import Web3, HTTPProvider

w3 = Web3(Web3.HTTPProvider("https://polygon-mumbai.infura.io/v3/d88fe2bed1a9459cbe2ad7a540290330"))
print(w3.eth.accounts)