from threading import current_thread
from src.core.component_blockchain.Transaction import Transaction
from src.core.component_blockchain.Block import Block
from src.infrastructure.Writer import Writer
from src.globals import MINING_DIFFICULTY,INIT_BLOCK
import json
from src.infrastructure.serializer import serialize



# Blockchain class defines the main structure of the blockchain and its functions
class Blockchain:
    """
    Class represent a blockchain with his parameters
    """

    def __init__(self):
        # The list of blocks that make up the blockchain
        self.chain=[]
        # The list of transactions in the current block
        self.transactions = []
        # The origin block is added to the blockchain
        ORIGIN_BLOCK=Block([],MINING_DIFFICULTY,0,init_block=INIT_BLOCK)
        self.chain.append(ORIGIN_BLOCK)

    # Converts the Blockchain object to a string in JSON format
    def __str__(self):
         return json.dumps(self,default=serialize)

    # Submits a block to the blockchain
    def submit_block(self,block):
        # Verify that all blocks in the chain are valid
        assert all([block.verify_block() for block in self.chain])
        # Check if the block is a valid addition to the chain
        valid=self.valid_chain(block)
        if not valid:
            raise Exception(f"block {block} from thread {current_thread().name} is not valid ! ")
        # Add the block to the chain
        self.chain.append(block)
        # Clear the list of transactions in the current block
        self.transactions=[]

    # Creates a block with proof of work
    def create_block_proof(self,hashPrevBlock,zeros=MINING_DIFFICULTY):
        return Block(transactions=self.transactions,zeros=zeros,hashPrevBlock=hashPrevBlock)

    # Adds a transaction to the list of transactions in the current block
    def set_transaction(self,transaction):
        # Check if the transaction is an instance of Transaction class
        assert isinstance(transaction,Transaction)
        # Verify the transaction
        assert transaction.verify_transaction()
        # Add the transaction to the list of transactions in the current block
        self.transactions.append(transaction)

    # Check if the block is a valid addition to the chain
    def valid_chain(self,block):
        # Check if the previous block hash matches the hash of the last block in the chain
        return block.header["HashPrevBlock"] == self.chain[-1].hash()


    # Writes the blockchain to a file
    def write(self,file_path="blockchain.json",mode="a"):
        # Create an instance of the Writer class
        writer=Writer(self,dict_method={"file_path":file_path})
        # Write the blockchain to the file specified
        writer.write(mode=mode)















