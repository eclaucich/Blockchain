
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