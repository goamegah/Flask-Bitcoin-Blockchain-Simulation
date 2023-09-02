import json
from Crypto.PublicKey import RSA
from src.core.component_blockchain.Transaction import Transaction
from src.core.component_blockchain.Block import Block
from hashlib import sha512
from src.globals import INIT_TRANSACTION,MINING_DIFFICULTY



if __name__=="__main__":
    transactions=[]
    for i in range(15):
        keyPair_sender=RSA.generate(bits=1024)
        keyPair_receiver=RSA.generate(bits=1024)
        s=keyPair_sender.n,keyPair_sender.e
        r=keyPair_receiver.n,keyPair_receiver.e
        transaction_wo_sign=json.dumps({"Transactions":INIT_TRANSACTION,"Sender key":s, \
                                        "Receiver key":r,"Amount":1,"Fees":0.01},default=str)
        msg=transaction_wo_sign.encode("utf-8")
        hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
        signature=pow(hash,keyPair_sender.d,keyPair_sender.n)
        t=Transaction(s,r,1,0.01,signature)
        transactions.append(t)
    bloc=Block(transactions=transactions,zeros=MINING_DIFFICULTY,hashPrevBlock=0)
    print(bloc)



