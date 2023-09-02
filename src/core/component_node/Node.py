import json
import threading
from hashlib import sha512
from queue import Queue
from time import sleep
from Crypto.PublicKey import RSA
from src.core.component_blockchain.Transaction import Transaction
from src.core.component_node.NewTransaction import NewTransaction
from src.globals import PORT_BEGIN, FEES, INIT_TRANSACTION, N, TIMEOUT, MINING_DIFFICULTY
from src.core.component_node.ThreadServer import ThreadServer
from src.core.component_node.ThreadClient import ThreadClient
from src.core.component_blockchain.Blockchain import Blockchain

class Node(threading.Thread):
    """
    This code is a part of a blockchain network simulation, implemented in Python.
    The main class "Node" creates nodes that act as both clients and servers, participating in the transaction and block creation process of the blockchain.
    The Node class inherits the threading.Thread class and starts the following threads:
    -thread_server, which creates a server for the node to receive incoming transactions from other nodes.
    -thread_listen_user_input, which listens for user input from the flask web application.
    -thread_handle_transaction, which handles incoming transactions.
    -thread_submit_block, which creates blocks and submits them to the blockchain.
    A blockchain object is created and stored in the node object, representing the blockchain for that particular node.
    A new_transaction object is also created to sychronize all nodes (in objective to have same blockchain for all nodes).
    Overall, the Node class creates nodes that can participate in the blockchain network by sending and receiving transactions and creating blocks.
    """
    number_nodes=N
    def __init__(self, id, thread_flask: threading.Thread, q:Queue, lock: threading.Lock):
        super().__init__()
        #id of node
        self.id=id
        #port_number, used for server of self node
        self.port_number=PORT_BEGIN+id
        #blockchain of self node
        self.blockchain=Blockchain()
        #new_transaction object is created, usefull in objective of sychronize all nodes
        self.new_transaction=NewTransaction(self.id,False)
        #thread_server, thread_flask instantiated
        self.thread_server=ThreadServer(port_number=self.port_number,blockchain=self.blockchain,new_transaction=self.new_transaction)
        self.thread_flask=thread_flask
        #objects for synchronization of all nodes.
        self.q=q
        self.lock=lock
        self.control_freq_transaction=False
        #list of incoming input of web user
        self.list_user_input=[]
        #coordinator created with None at the beginning
        self.coord=None



    def run(self):
        """
        The run method starts the threads and begins the node's operation in the blockchain network.
        """
        self.thread_server.start()
        sleep(3)
        thread_listen_user_input=threading.Thread(target=self.listen_user_input)
        thread_listen_user_input.start()

        thread_handle_transaction=threading.Thread(target=self.handle_transaction)
        thread_handle_transaction.start()

        thread_submit_block=threading.Thread(target=self.create_block)
        thread_submit_block.start()

    def create_block(self):
        """
        The create_block thread creates blocks by calling the create_block_proof method of the blockchain object:
        It find proof of work (sha512 hashes), a specific nonce that satisfies the MINING_DIFFICULTY condition and update block with nonce found.
        If the node is the coordinator, the specific nonce and blockchain updated is sent back to the flask web application.
        For all nodes: blockchain is also written to a json file for persistence.
        """
        while True:
            # wait for 1 second
            sleep(1)
            # check if a new transaction can be insert in blockchain block
            if self.new_transaction.bool_transaction:
                # create a new block from the last block in the blockchain
                block=self.blockchain.create_block_proof(self.blockchain.chain[-1].hash())
                valid=False
                noncel=0
                remote_nonce=False
                # loop until a valid nonce is found
                while not valid:
                    if not self.q.empty():
                        # get the nonce from the queue if it's not empty
                        noncer=self.q.get()
                        nonce=noncer
                        remote_nonce=True
                    else:
                        # increment the nonce if the queue is empty
                        noncel+=1
                        nonce=noncel
                    # create the guess by concatenating the block's string representation and the nonce
                    guess=(block.str_proof()+str(nonce)).encode("utf-8")
                    # create a hash of the guess using SHA-512
                    guess_hash=sha512(guess).hexdigest()
                    # check if the guess hash meets the mining difficulty
                    valid=guess_hash[:int(MINING_DIFFICULTY/4)] == "0" * int(MINING_DIFFICULTY/4) #(MINING_DIFFICULTY/4)*4(each hexadecimal character encoded with 4 bits)
                    if valid == True:
                        if remote_nonce==False:
                            # add the nonce to the queue if it's not from a remote node
                            with self.lock:
                                if self.q.empty():
                                    self.q.put(nonce)
                                else:
                                    nonce=self.q.get()
                        break
                # set the nonce for the block
                block.set_nonce(nonce)
                # submit the block to the blockchain
                self.blockchain.submit_block(block)
                # reset the new transaction flag
                self.new_transaction.bool_transaction=False
                # write the blockchain to a file
                self.blockchain.write(file_path=f"noeud{self.id}_blockchain.json",mode="w")
                # check if the node is the coordinator node
                if int(self.coord)==int(self.id):
                    # remove the first item in the list of user inputs
                    self.list_user_input.pop(0)
                    # update the blockchain and nonce in the thread_flask object
                    self.thread_flask.back["blockchain"]=self.blockchain
                    self.thread_flask.back["nonce"]=nonce
                    # wait for other nodes to finish
                    sleep(3)
                    # reset the control frequency flag for transactions
                    self.control_freq_transaction=False


    #The listen_user_input thread listens for input from the flask web application.
    def listen_user_input(self):
        while True:
            sleep(0.5)
            # retrieve the user input from the thread_flask object
            user_input=self.thread_flask.user_input
            #format user_input=(coordinator,amount_of_transaction)
            if user_input:
                # set the coordinator to self.coord to the first element of the user input tuple
                self.coord=user_input[0]
                # check if user input sent a transaction with only amount of transaction
                if user_input[1]:#user_input[1]=amount of user transaction
                    #if node is the coordinator
                    if int(self.id)==int(self.coord):
                        # add the user input to the list_user_input attribute
                        self.list_user_input.append(user_input)
                        self.thread_flask.user_input=self.thread_flask.user_input[0],None


    #The handle_transaction thread processes transactions incoming by flask web user and adds them to blockchain.
    def handle_transaction(self):
        while True:
            sleep(1)
            #check if the node is the coordinator
            if self.coord:
                # confirm the node id matches the coordinator id
                if int(self.id)==int(self.coord):
                    while self.control_freq_transaction:
                        sleep(1)#process another transaction t at this time: wait the transaction t to finish
                    if len(self.list_user_input):
                        #flag control_freq_transaction for handle_transaction thread:
                        #using to process one and only one user transaction at the same time for all nodes
                        self.control_freq_transaction=True
                        # get the first user input in the list
                        user_input=self.list_user_input[0]
                        coordinator,amount=user_input
                        # create a new transaction
                        transaction=self.create_transaction(int(amount))
                        # broadcast the transaction to the network
                        self.broadcast_message(str(transaction))
                        # broadcast message confirmation: the current transaction has sent to all nodes
                        self.broadcast_message(f"#OK for transaction#:{str(transaction)}")
                        # add the transaction to the current list of transaction in blockchain
                        self.blockchain.set_transaction(transaction)
                        # increase the count of transactions
                        self.new_transaction.count_transactions+=1
                        # set the boolean value to indicate a new incoming transaction has been made
                        # --> flag for create_block thread
                        self.new_transaction.bool_transaction=True




    def broadcast_message(self,message:str) -> bool:
        #Initialize timeout value to zero
        timeout=0
        #create a dictionary of sent (see send method) messages from the current node to all other nodes excluding itself
        sends={i:self.send(PORT_BEGIN+i,str(message)) for i in range(self.number_nodes) if i != self.id}
        while not all(sends.values()) and timeout < TIMEOUT:
            # Loop through the dictionary until all messages are sent or timeout value is reached
            sends={i:self.send(PORT_BEGIN+i,str(message)) for i in range(self.number_nodes) if i != self.id}
            timeout+=1
        # If all messages are not sent and timeout value has been reached
        if not all(sends.values()) and timeout == TIMEOUT:
            raise Exception(f"Sending message to all nodes from {self.id} failed:{sends}")
        #all(sends.values()) is True
        return True



    def send(self,port_number,data:str):
        """
        :param port_number: port_number of node receiver the message
        :param data: message from node sender to node receiver
        method who create thread to send message for 2 nodes:
        return True if and only if message has been received by receiver node
        """
        thread_client=ThreadClient(port_number,data)
        thread_client.start()
        thread_client.join()
        return thread_client.ack

    # This code is for creating a transaction.
    def create_transaction(self,amount,transactions=INIT_TRANSACTION):
        # Generate the sender and receiver keys using RSA
        keyPair_sender=RSA.generate(bits=1024)
        keyPair_receiver=RSA.generate(bits=1024)
        # Store the public key of the sender and receiver
        s=keyPair_sender.n,keyPair_sender.e
        r=keyPair_receiver.n,keyPair_receiver.e
        # Set the fees for the transaction
        fees=FEES
        # Create a JSON string that contains the transaction details
        transaction_wo_sign=json.dumps({"Transactions":transactions,"Sender key":s, \
                                "Receiver key":r,"Amount":amount,"Fees":fees},default=str)
        # Hash the transaction using SHA-512
        hash=int.from_bytes(sha512(transaction_wo_sign.encode("utf-8")).digest(),byteorder="big")
        # Sign the transaction using the private key of the sender
        signature=pow(hash,keyPair_sender.d,keyPair_sender.n)
        # Return the final transaction object
        return Transaction(s,r,amount,FEES,signature,transactions)
















