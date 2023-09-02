import json
import threading

from src.core.component_blockchain.Blockchain import Blockchain
from src.core.component_blockchain.Transaction import Transaction
from src.core.component_node.NewTransaction import NewTransaction


class ThreadConnection(threading.Thread):
    """
    This class is a class for thread connection.
    It implements a threading class to handle multiple clients connecting to a thread server.
    """
    # A class variable to store the transaction string
    transaction_str=""
    def __init__(self,blockchain:Blockchain,conn,new_transaction:NewTransaction):
        threading.Thread.__init__(self)
        self.blockchain=blockchain # Blockchain object
        self.conn=conn # Connection object
        self.new_transaction=new_transaction # NewTransaction object

    def run(self):
        try:
            # Receiving the message from the client
            message=self.receive_message_from_client()
            # Checking if the message starts with '#' symbol
            if message[0]=="#":
                #Case of message from coordinator to tell that transaction has been broadcasting to all nodes
                # Adding the transaction to the blockchain
                self.blockchain.set_transaction(Transaction(**json.loads(ThreadConnection.transaction_str)))
                # Setting the boolean value of the new transaction to True:
                # flag for a specific thread (in Node class) to process this transaction
                self.new_transaction.bool_transaction=True
                # Increasing the count of transactions
                self.new_transaction.count_transactions+=1
            else:
                # Storing the incoming transaction string (from client) in the class variable
                ThreadConnection.transaction_str=message
            # Sending the response to the client (acknowledgement)
            self.send_response_to_client("True")
        except Exception as e:
            print(f"Error from {self.conn}:{e}")

    # Method for receiving the message from the client
    def receive_message_from_client(self):
        # Receiving the message and decoding it
        message = self.conn.recv(2048).decode() #maximum bytes received from client is 2048
        return message

    # Method for sending message to the client (associated with the connection: conn variable)
    def send_response_to_client(self,message):
        # Encoding the message and sending it
        self.conn.sendall(message.encode())





