from src.globals import INIT_TRANSACTION

def serialize(obj):
    from src.core.component_blockchain.Transaction import Transaction
    from src.core.component_blockchain.Block import Block
    from src.core.component_blockchain.Blockchain import Blockchain
    # Check if the object passed is a Transaction instance
    if isinstance(obj, Transaction):
        # Check if the transactions attribute of the Transaction object is equal to INIT_TRANSACTION
        if obj.transactions == INIT_TRANSACTION:
            return obj.__dict__
        else:
            # Create a dictionary with the attributes of the Transaction object
            dict_transac = {
                "transactions": [serialize(t) for t in obj.transactions],
                "sender_key": obj.sender_key,
                "receiver_key": obj.receiver_key,
                "amount": obj.amount,
                "fees": obj.fees,
                "sign": obj.sign
            }
            return dict_transac

    # Check if the object passed is a Block instance
    if isinstance(obj,Block):
        # Return a dictionary with the attributes of the Block object
        return {
            "transactions":[serialize(t) for t in obj.transactions],
            "transaction_counter":obj.transaction_counter,
            "header":obj.header
        }

    # Check if the object passed is a Blockchain instance
    if isinstance(obj,Blockchain):
        # Return a dictionary with the attributes of the Blockchain object
        return {
            "chain": [serialize(c) for c in obj.chain],
            "transactions": [serialize(t) for t in obj.transactions]
        }


