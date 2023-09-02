import json


class NewTransaction:
    """
    NewTransaction object used for synchronization of all nodes
    """
    def __init__(self,node_id:int,bool_transaction:bool):
        #node_id for a node
        self.node_id=node_id
        #bool_transaction flag: see Node class to understand this attribute
        self.bool_transaction=bool_transaction
        #number of transaction for a coordinator node
        self.count_transactions=0

    #str representation for NewTransaction object
    def __str__(self):
        return json.dumps(self.__dict__)
