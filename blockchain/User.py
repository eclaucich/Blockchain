import json
from Blockchain import Blockchain
from Block import Block
from Transaction import Transaction
import rsa
import numpy as np

##
##
## User represents someone that has a wallet in an crypto exchange 
##
##


class User:
    def __init__(self, alias:str, centralNode) -> None:
        self.alias = alias # For simple debug uses
        self.currentBlock:Block = None # Current block beign mined
        self.centralNode = centralNode # Node use to comunicate to other nodes
        (self.pk, self.sk) = rsa.newkeys(512) # public and secret key to sign transactions
        self.blockchain:Blockchain = self.centralNode.GetBlockchain() # Copy of the blockchain on this node
        self.centralNode.AddNode(self) # Comunicate to the central node that we are a node now (It simulates how a node will comunicate via TCP to negihboards)

    
    # Recieves a transaction that has been broadcasted in the network by other nodes
    # The transaction is added as a pending transaction in this node's blockchain
    def BroadcastedTransaction(self, transaction:Transaction):
        self.blockchain.transactions.append(transaction)


    # Recieves a block that has been broadcasted in the network by other nodes
    # If the block is valid is added to this node's blockchain and returns 1 possitive vote
    # If is not valid returns 0 votes
    def BroadcastedBlock(self, block:Block):
        if block.IsValid():
            self.blockchain.chain.append(block) # Add block to the blockchain
            if self.currentBlock != None: # If this node was working in a block, it needs to start over using the new block as the last block
                self.MinePendingBlockTransactions(self.currentBlock) # Starts mining the same transactions as before
            return 1 #Returns 1 possitve vote
        else:
            return 0 # The block is invalid, returns 0 votes

    
    # A block broadcasted by this node was accepted by the network
    def BlockAccepted(self):
        if self.currentBlock == None: # Just to check if something strange happened. This should never happend.
            print("The user {} had a block accepted but it has none pending block".format(self.alias))
        else:
            self.blockchain.chain.append(self.currentBlock) #The block was accepted so it is added to the blockchain
            self.currentBlock = None
            

    # A block broadcasted by this node was rejected by the network
    def BlockDenied(self):
        print("Broadcasted block from {} was rejected".format(self.alias))
        self.currentBlock = None

    
    # Allows a User to exchange fiat currency for the blockchain cripto
    # It creates a transactions that goes from the system (None) to the user with the corresponding amount of coins
    def BuyCoins(self, amount):
        tx = Transaction(None, self.pk, amount)
        self.blockchain.transactions.append(tx)
        self.centralNode.NewTransaction(tx, self)

    
    # Allows a User to send currency to another account
    def CreateNewTransaction(self, toUser, amount:int):
        if self.GetBalance() < amount: #If the user sending the currency has in his balance less than its beeign transfer, its invalid
            print("Invalid transaction, not enough resources in your wallet")
            return

        # Creates the transaction, sign it, adds it to the pending transactions and broadcast it
        tx = Transaction(self.pk, toUser.pk, amount)
        tx.Sign(self.sk)
        self.blockchain.transactions.append(tx)
        self.centralNode.NewTransaction(tx, self)


    # Allows the User to mine a block with certain transactions
    # txIdxs its an array of indexes representing the indexes of transactions in the pending transactions list    
    def MinePendingTransactions(self, txIdxs):
        lastBlockNumber = self.blockchain.chain[-1].blockNumber # Get the last block's number
        blockNumber = lastBlockNumber+1 # The number of the new block
        txs = np.array(self.blockchain.transactions)[txIdxs] # Sub-array of transactions beeing added to the block
        self.currentBlock = Block(blockNumber, txs, self.blockchain.chain[lastBlockNumber].hash, self.blockchain.difficulty) # Creates a new block

        self.currentBlock.Mine() # Starts mining the block
        self.centralNode.NewBlock(self.currentBlock, self) # Once ends mining it broadcast the block to the central node


    # Creates a new block with the same transactions as oldBlock but updating the hash of the last block
    def MinePendingBlockTransactions(self, oldBlock:Block):
        blockNumber = oldBlock.blockNumber+1
        txs = oldBlock.transactions
        self.currentBlock = Block(blockNumber, txs, oldBlock.hash)


    # Displays a json with some information of this user's blockchain and pending transactions
    def ShowBlockchain(self):
        print(json.dumps(self.blockchain.ShowBlockchain(self.alias), indent=2))


    # Calculates the balance on the account
    def GetBalance(self):
        balance = 0
        for b in self.blockchain.chain: # For each block in this blockchain
            for tx in b.transactions: # For each transaction in each block
                if tx.fromAddress == self.pk:
                    balance -= tx.amount # If in the transaction this user sended the money, decrease the balance
                elif tx.toAddress == self.pk:
                    balance += tx.amount # If in the transaction this user recieved the money, increse the balance
        return balance

