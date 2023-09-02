#This file is entry point of the program, just run: python app.py to run the main program

import threading
from src.core.component_node.Node import Node
from src.globals import N
from queue import Queue
from src.web.ThreadFlask import ThreadFlask

if __name__=="__main__":
    q=Queue(maxsize=1)
    lock= threading.Lock()
    thread_flask=ThreadFlask()
    thread_flask.start()
    nodes=[]
    for i in range(N):
        nodes.append(Node(i,thread_flask,q,lock))
    [node.start() for node in nodes]
