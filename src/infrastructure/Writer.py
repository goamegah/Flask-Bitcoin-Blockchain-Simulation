class Writer:
    """
    This class is used to write data object with a specific method.
    """
    def __init__(self,data:object,method:str="disk local file",dict_method:dict={"file_path":"file.data"}):
        # initialize variables
        self.dict_method=dict_method
        self.method=method
        self.data=data

    def write(self,mode="a"):
        # if the method is to write to a disk local file
        if self.method == "disk local file":
            with open(self.dict_method["file_path"],mode) as f:
                # open the specified file using the specified mode and write the data
                f.write(str(self.data))
