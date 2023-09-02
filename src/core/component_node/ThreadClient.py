import threading
import socket

class ThreadClient(threading.Thread):
    """
    Class for creating a client thread
    """
    def __init__(self,port_number:int,data:str):
        threading.Thread.__init__(self)
        #port_number of thread server: client contact this thread server
        self.port_number=port_number
        #message sent by client to server
        self.data=data
        #acknowledgement of message
        self.ack=False

    # Run method to send data to the server
    def run(self):
        # Host and port details
        host,port=("localhost",self.port_number)
        # Create a socket object
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            # Connect to the server using the host and port details
            s.connect((host,port))
            # Encode the data to be sent
            data=self.data.encode("utf-8")
            # Send the data to the server
            s.sendall(data)
            # Receive the ack from the server
            ack=s.recv(1024).decode()
            assert ack=="False" or ack == "True"
            if ack=="True":
                self.ack=True
        except ConnectionRefusedError:
            # Catch the ConnectionRefusedError if the server is not available
            print(f"Connection refused for server{self.port_number}")
        finally:
            #close the communication
            s.close()

