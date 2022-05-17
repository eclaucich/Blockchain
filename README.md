# Blockchain
 A simple emplementation of a blockchain in Python

---

## How to use

### Central node
A central node is needed so the information can be broadcasted to the whole network of nodes
```python
centralNode = CentralNode()
```

### User
Each user represents an account that can be part of a transaction
```python
user1 = User(alias="User1", centralNode=centralNode)
```
#### Buying coins
This adds a transaction from the system to the user. It allows to test the network more easily. (The transaction needs to be mined)
```python
user1.BuyCoins(100)
```
#### Mine transactions
The user can select pending transactions by its indexes and mine a block.
```python
user1.MinePendingTransactions([0])
```
#### Creating transactions
A user can create transactions to any other user. If its valid, it gets broadcasted to the network.
```python
user2 = User(alias="User2", centralNode=centralNode)
user1.MinePendingTransactions([0, 1])
```

#### Debuging current state of blockchain in a node (The idea is that each node always agrees on the same blockchain)
```python
user1.ShowBlockchain()
```

### Complete test code
```python
from CentralNode import CentralNode
from User import User


def main():
    centralNode = CentralNode()

    user1 = User(alias="User1", centralNode=centralNode)
    user2 = User(alias="User2", centralNode=centralNode)


    user1.BuyCoins(100)

    user1.MinePendingTransactions([0])

    user1.CreateNewTransaction(user2, 30)

    user1.MinePendingTransactions([0, 1])

    centralNode.ShowBlockchain()
    user1.ShowBlockchain()
    user2.ShowBlockchain()


if __name__ == "__main__":
    main()
```
