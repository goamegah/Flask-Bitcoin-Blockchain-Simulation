import threading
from flask import Flask, request, render_template, redirect, url_for
import src.globals as globals
from src.web.FlaskAppWrapper import FlaskAppWrapper




class ThreadFlask(threading.Thread):
    """
    Class for creating flask thread which is web interface of the app
    """

    def __init__(self):
        threading.Thread.__init__(self)
        # Create a Flask application instance
        self.app=Flask(__name__)
        # Variable to store user inputs
        self.user_input=None
        # Dictionary to store backend values: from application backend
        self.back={}

    def run(self):
        # Create an instance of FlaskAppWrapper
        flask_wrapper=FlaskAppWrapper(self.app)
        # Add endpoints to the Flask application
        flask_wrapper.add_endpoint('/', 'root', self.choose_number_nodes, methods=["GET","POST"])
        flask_wrapper.add_endpoint('/choose', 'choose', self.select_coordinator_index, methods=["GET","POST"])
        flask_wrapper.add_endpoint('/transactions', "transactions", self.create_transaction_index, methods=["GET","POST"])
        flask_wrapper.add_endpoint('/blockchain', "blockchain", self.display_block_index, methods=["GET"])
        # Start the Flask application
        flask_wrapper.run()

    # Method to handle the request to choose the number of nodes
    def choose_number_nodes(self):
        if request.method == 'POST':
            # Get the number of nodes from the form data
            number_nodes = request.form['number_nodes']
            # Store the number of nodes in the globals.py file
            globals.N=number_nodes
            # Redirect to the next endpoint
            return redirect(url_for("choose"))
        # Render the template for choosing the number of nodes
        return render_template("index_main.html")

    # Method to handle the request to choose the coordinator node
    def select_coordinator_index(self):
        if request.method == 'POST':
            # Get the coordinator node from the form data
            coordinator = request.form['coordinator']
            # Store the coordinator node in the user_input variable
            self.user_input=(coordinator,None)
            # Redirect to the next endpoint
            return redirect(url_for("transactions"))
        # Render the template for choosing the coordinator node
        return render_template("index_choose_node.html",number_of_nodes=globals.N)

    # Method to handle the request to create transactions
    def create_transaction_index(self):
        if request.method == 'POST':
            # Get the transaction amount from the form data
            amount = request.form['amount']
            # Store the transaction amount in the user_input variable:self.user_input=(coordinator,amount)
            self.user_input=self.user_input[0],amount
            # Redirect to the next endpoint
            return redirect(url_for("transactions"))
        if "nonce" in self.back.keys():
            #if nodes found nonce for Proof of Work: nonce value displayed in web page
            return render_template("index_create_transactions.html",number_of_nodes=globals.N,nonce=self.back["nonce"])
        # Render the template for create transaction in blockchain
        return render_template("index_create_transactions.html",number_of_nodes=globals.N,nonce="NaN")


    def display_block_index(self):
        # Check if the key "blockchain" exists in the backend (self.back)
        if "blockchain" in self.back.keys():
            # Return the value of the "blockchain" key as a string
            return str(self.back["blockchain"])
        # Return a message indicating that the blockchain has not been created
        return "Blockchain has not been created"













