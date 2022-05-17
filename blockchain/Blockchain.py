import json
from Block import Block

#
#
# Represents a blockchain
#
#

class Blockchain:
    def __init__(self) -> None:
        self.difficulty = 4 # Number of 0 needed at the start of the hash of a block to be valid
        self.chain = [self.GenesisBlock()] #The blockchain always starts with an empty block
        self.transactions = [] #List of pending transcations
        self.mineReward = 10


    # Creates the genesis block
    def GenesisBlock(self):
        genesis = Block(0, [], None, self.difficulty)
        genesis.Mine()
        return genesis


    # Removes a list of transactions from the pending transcations
    def RemoveTransactions(self, txs):
        newTransactions = [] # New array of transactions
        
        for tx in self.transactions:
            remove = False
            for rtx in txs:
                if tx.signature == rtx.signature: # Removes the transaction if it is one of the removed
                    remove = True
                    break
            
            if not remove:
                newTransactions.append(tx)

        self.transactions = newTransactions



    # Creates a JSON with some useful information of the blockchain and transaction
    def ShowBlockchain(self, alias:str):
        
        info = "{\""+alias+"\":{\"blocks\":["
        
        # For each block
        for ic, c in enumerate(self.chain):
            block_str = "{\"number\": " + str(c.blockNumber) + "," + "\"prev\": \"" + str(c.hashPrev) + "\"," + "\"hash\": \"" + str(c.hash) + "\"," + "\"txs\":["
            tx_str = ""
            for it, t in enumerate(c.transactions):
                if t.fromAddress == None:
                    tx_str = "{\"from\": \"" + str(t.fromAddress) + "\"," + "\"to\": \"" + str(t.toAddress.n) + "\"," + "\"amount\":" + str(t.amount) + "}"
                else:
                    tx_str = "{\"from\": \"" + str(t.fromAddress.n) + "\"," + "\"to\": \"" + str(t.toAddress.n) + "\"," + "\"amount\":" + str(t.amount) + "}"
                if it < len(c.transactions)-1:
                    tx_str += ","
            tx_str += "]}"
            block_str += tx_str
            if ic < len(self.chain)-1:
                block_str += ","
            
            info += block_str
        info += "],\"pending\":["
        
        # For each pending transaction
        for it, t in enumerate(self.transactions):
            if t.fromAddress == None:
                tx_str = "{\"from\": \"" + str(t.fromAddress) + "\"," + "\"to\": \"" + str(t.toAddress.n) + "\"," + "\"amount\": " + str(t.amount) + "}"    
            else:
                tx_str = "{\"from\": \"" + str(t.fromAddress.n) + "\"," + "\"to\": \"" + str(t.toAddress.n) + "\"," + "\"amount\": " + str(t.amount) + "}"
            if it < len(self.transactions)-1:
                tx_str += ","
            info += tx_str
        
        info += "]"+"}"+"}"

        return json.loads(info)
