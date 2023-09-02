import json
from src.core.component_blockchain.Transaction import Transaction
from hashlib import sha512
from src.infrastructure.serializer import serialize


class Block:
    """
    Class represent a block for a blockchain
    """

    def __init__(self,transactions:list[Transaction],zeros:int,hashPrevBlock:int,init_block=False,nonce:int=-1):
        """
        :param transactions: list of immutable transaction
        :param nonce: nonce for Proof of Work
        :param hashPrevBlock: hash of previous block
        :param zeros: Number of zeros required for resolving Proof of Work
        :param init_block: Boolean value indicating if this is an initialization block (usefull for Blockchain Class)
        """
        # If this is not an initialization block
        if init_block==False:
            # Set the transactions list
            self.transactions=transactions
            # Set the transaction counter
            self.transaction_counter=len(transactions)
            # Set the header with the given parameters
            self.header={
                "HashPrevBlock":hashPrevBlock,
                "Nonce":nonce,
                "Zeros":zeros
            }
            # Verify the validity of block
            assert self.verify_block()
        # If this is an initialization block
        else:
            # Set an empty transactions list
            self.transactions=[]
            # Set the transaction counter to 0
            self.transaction_counter=0
            # Set an empty header
            self.header={
            }

    # Method to return a string representation of the Block object
    def __str__(self):
        # Return a serialized version of the object as a string with serialize function
        return json.dumps(self,default=serialize)

    # Method to return a string representation of the Proof of Work part of the block
    def str_proof(self):
        # Copy the header without the nonce
        header_wo_nonce=self.header.copy()
        del header_wo_nonce["Nonce"]
        # Return a serialized version of the transactions list, transaction counter, and header without the nonce
        return json.dumps({"Transactions":self.transactions,"Transaction Counter":self.transaction_counter, \
                           "Header":header_wo_nonce},default=str)

    def verify_block(self):
        """
        Verifies if the block is not corrupted
        """
        valid=True
        for t in self.transactions:
            valid=valid and isinstance(t,Transaction)
            if not valid:
                return False
            else:
                valid=t.verify_transaction()
            if not valid:
                return False
        return valid

    def hash(self):
        """
        This method returns the hash of the current block with SHA512 hash function
        """
        return int.from_bytes(sha512(str(self).encode("utf-8")).digest(), byteorder='big')

    def set_nonce(self,nonce):
        """
        param nonce: nonce of block
        Set nounce of nonce of self
        """
        self.header["Nonce"]=nonce








