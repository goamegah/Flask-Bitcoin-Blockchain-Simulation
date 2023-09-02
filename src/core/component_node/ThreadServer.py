import threading
import socket

from src.core.component_node.NewTransaction import NewTransaction
from src.core.component_node.ThreadConnection import ThreadConnection
from src.core.component_blockchain.Blockchain import Blockchain

class ThreadServer(threading.Thread):
    """
    Class for thread server
    """
    def __init__(self,port_number:int,blockchain:Blockchain,new_transaction:NewTransaction):
        threading.Thread.__init__(self)
        # Assigning the port number for the server
        self.port_number=port_number
        # Assigning the blockchain for the server
        self.blockchain=blockchain
        #new transaction object using for synchronization of all nodes
        self.new_transaction=new_transaction

    # Method to run the server
    def run(self):
        # Host and port are set to empty string and self.port_number respectively
        host,port=("",self.port_number)
        # Creating a socket with the specified parameters
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # Binding the socket to the host and port
        s.bind((host,port))
        while True:
            # Listening clients requests
            s.listen(5)
            # Accepting the request and getting the address of the client
            conn,adress=s.accept()
            # Creating a thread connection object with blockchain, connection and new transaction object
            thread_client=ThreadConnection(blockchain=self.blockchain,conn=conn,new_transaction=self.new_transaction)
            # Starting the thread for the connection
            thread_client.start()


