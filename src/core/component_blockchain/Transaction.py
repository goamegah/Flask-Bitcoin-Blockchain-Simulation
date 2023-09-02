from hashlib import sha512
import json
from src.globals import INIT_TRANSACTION
from src.infrastructure.serializer import serialize
class Transaction:
    """
    Class represent a blockchain transaction with his parameters
    """

    def __init__(self,\
        sender_key:tuple,receiver_key:tuple,amount:float,fees:float,sign:int,transactions:list=INIT_TRANSACTION):
        """
        :param sender_key: public key of sender
        :param receiver_key: public key of receiver
        :param amount: amount of transaction
        :param fees: fees of transaction
        :param sign: int represent signature
        :param transactions: list of transactions t which t.receiver_key=self.sender_key if transactions set by user
        """
        (ns,ds)=sender_key
        (nr,dr)=receiver_key
        # Check if the values of ns resp nr and ds resp dr are positive integers
        assert ns>0 and nr >0 and ds > 0 and dr >0
        # Store the transactions, sender_key, receiver_key, amount, fees, and sign
        self.transactions=transactions
        self.sender_key=sender_key
        self.receiver_key=receiver_key
        self.amount=amount
        self.fees=fees
        self.sign=sign
        # Check if the fees and amount are non-negative
        assert fees >=0 and amount>=0
        # Verify the transaction
        assert self.verify_transaction()

    def __str__(self):
        """
        Returns a string representation of the transaction in JSON format
        """
        return json.dumps(self,default=serialize)

    def str_signature(self):
        """
        Returns a string representation of the transactions, sender_key, receiver_key, amount, and fees
        """
        return json.dumps({"Transactions":self.transactions,"Sender key":self.sender_key, \
            "Receiver key":self.receiver_key,"Amount":self.amount,"Fees":self.fees},default=str)

    def verify_transaction_amount(self):
        """
        Returns a boolean indicating whether the sender has enough bitcoins to send.
        If self.transactions==INIT_TRANSACTION (constant), return always True
        """
        if self.transactions==INIT_TRANSACTION:
            return True
        total_amount=0
        for t in self.transactions:
            if t.receiver_key != self.sender_key:
                return False
            total_amount+=t.amount
        return total_amount >= self.amount + self.fees

    def verify_transaction_signature(self):
        """
        Verifies the signature of the transaction. Using RSA algorithm do encrypt transaction
        """
        msg=self.str_signature()
        hashMsg = int.from_bytes(sha512(msg.encode("utf-8")).digest(), byteorder='big')
        hashFromSign=pow(self.sign,self.sender_key[1], self.sender_key[0]) #pow(signature,d,n)
        return hashMsg==hashFromSign

    def verify_transaction(self):
        """
        Return a boolean value to indicate if signature/amount of transaction is valid
        """
        return self.verify_transaction_signature() and self.verify_transaction_amount()










