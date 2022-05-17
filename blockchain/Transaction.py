import rsa

#
#
# A transaction in the blockchain
#
#


class Transaction:
    def __init__(self, fromAddress, toAddress, amount):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount
        self.signature = None


    # A user sign the transaction so it can be validated after by any other user
    # Its composed by the address and amount 
    def Sign(self, sk):
        self.signature = rsa.sign((str(self.fromAddress)+str(self.toAddress)+str(self.amount)).encode(), sk, hash_method='SHA-256')

    
    # Validation of the signature
    def Validate(self, pk):
        if self.signature == None: # If the transaction does not have a signature its invalid or its from the system TODO: how to make this more reliable?
            print("WARNING: The transaction has no signature")
        else: #If the encription method is SHA-256 is a valid signature
            return rsa.verify((str(self.fromAddress)+str(self.toAddress)+str(self.amount)).encode(), self.signature, pk)=='SHA-256'
