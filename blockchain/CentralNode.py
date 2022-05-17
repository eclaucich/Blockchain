import json
from User import User
from Blockchain import Blockchain
from Block import Block
from Transaction import Transaction
from copy import deepcopy

#
#
# This represents a node that its always updated, so is a safe way to broadcast and ask for information
#
#


class CentralNode:
    def __init__(self) -> None:
        self.blockchain = Blockchain() # The blockchain is initialized on this node
        self.nodes = [] # All the other nodes in the network


    # Returns a copy of the current state of the blockchain
    def GetBlockchain(self):
        return deepcopy(self.blockchain)


    # An User is added to the network
    def AddNode(self, user:User):
        self.nodes.append(user)


    # Broadcast a block to the rest of the nodes
    def BroadcastTransaction(self, transaction, user):
        for n in self.nodes:
            if n == user: # Not broadcasted to the origin node
                continue
            
            n.BroadcastedTransaction(transaction)


    # Broadcast a block to the rest of the nodes
    # A block is accepted if it has at least the 50% of the votes of the network
    def BroadcastBlock(self, block, user):
        votes = 0
        for n in self.nodes:
            if n == user: # Not broadcasted to the origin node
                continue
                
            votes += n.BroadcastedBlock(block) # Get the vote for each node
        
        if votes >= (int)(len(self.nodes)/2): 
            return True # Block accepted
        else:
            return False # Block rejected


    # Recieves a transaction from a user and broadcast it to the rest of the nodes
    def NewTransaction(self, tx:Transaction, fromUser:User):
        self.blockchain.transactions.append(tx)
        self.BroadcastTransaction(tx, fromUser)

    
    # Recieves a block from a user and broadcast it to the rest of the nodes
    def NewBlock(self, block:Block, fromUser:User):
        if self.BroadcastBlock(block, fromUser): # The broadcasted block was accepted by the network
            
            fromUser.BlockAccepted() # Informs to the origin user that the block was accepted

            self.blockchain.chain.append(block) # Add the block to this blockchain

            self.RemovePendingTransactions(block.transactions) # The transactions in the accepted block are removed from the pending transactions

            # Creates a transaction with the reward of the mined block to the origin user
            rewardTx = Transaction(None, fromUser.pk, self.blockchain.mineReward)
            self.NewTransaction(rewardTx, None)
            
        else:
            fromUser.BlockDenied() #Informs to the origin user that the block was rejected


    # Removes a list of transactions from the pending transactions
    def RemovePendingTransactions(self, transactions):
        self.blockchain.RemoveTransactions(transactions)
        for n in self.nodes:
            n.blockchain.RemoveTransactions(transactions) # Removes the same transactions on each node


    # Displays a json with some information of this user's blockchain and pending transactions
    def ShowBlockchain(self):
        print(json.dumps(self.blockchain.ShowBlockchain("Central"), indent=2))
