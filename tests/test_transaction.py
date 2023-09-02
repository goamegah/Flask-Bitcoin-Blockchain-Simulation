import json
from Crypto.PublicKey import RSA
from src.core.component_blockchain.Transaction import Transaction
from hashlib import sha512
from src.globals import INIT_TRANSACTION,FEES
import random
if __name__=="__main__":
    for i in range(25):
        keyPair_sender=RSA.generate(bits=1024)
        keyPair_receiver=RSA.generate(bits=1024)
        s=keyPair_sender.n,keyPair_sender.e
        r=keyPair_receiver.n,keyPair_receiver.e
        transaction_wo_sign=json.dumps({"Transactions":INIT_TRANSACTION,"Sender key":s, \
                                    "Receiver key":r,"Amount":1.2,"Fees":FEES},default=str)
        msg=transaction_wo_sign.encode("utf-8")
        hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
        signature=pow(hash,keyPair_sender.d,keyPair_sender.n)
        t=Transaction(s,r,1.2,FEES,signature)
        print(f"Test to verify transaction (INIT transaction) validity {i+1}:OK")
        amount=random.random()
        sender=r
        receiver=s
        fees=FEES
        transaction_wo_sign=json.dumps({"Transactions":[t],"Sender key":sender, \
                                        "Receiver key":receiver,"Amount":amount,"Fees":fees},default=str)
        msg=transaction_wo_sign.encode("utf-8")
        hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
        signature=pow(hash,keyPair_receiver.d,keyPair_receiver.n)
        t1=Transaction(sender,receiver,amount,fees,signature,transactions=[t])
        print(f"Test to verify transaction (transaction with attributes transactions not empty) validity {i+1}:OK")









