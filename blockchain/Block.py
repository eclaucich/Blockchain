from hashlib import sha256

#
#
# A block in the blockchain
#
#

class Block:
    def __init__(self, blockNumber, transactions, hashPrev, difficulty) -> None:
        self.hash = None 
        self.transactions = transactions # List of transactions
        self.nonce = 0 
        self.hashPrev = hashPrev # Has of the previous block
        self.blockNumber = blockNumber # Current block number
        self.difficulty = difficulty # Number of 0 needed at the start of the hash to be valid

    
    # Allows to mine this block
    def Mine(self):
        #Calculates the hash with the block number, list of transactions, previous block hash and nonce
        self.hash = sha256((str(self.blockNumber) + str(self.transactions) + str(self.hashPrev) + str(self.nonce)).encode()).hexdigest()
        while self.hash[:self.difficulty] != "0"*self.difficulty: # Iterates until the hash is valid
            self.nonce += 1
            self.hash = sha256((str(self.blockNumber) + str(self.transactions) + str(self.hashPrev) + str(self.nonce)).encode()).hexdigest()

    
    # A block is valid if the hash is valid, every transaction is valid and the previous hash is correct
    def IsValid(self):
        return True