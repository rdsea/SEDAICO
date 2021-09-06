from pymongo import MongoClient

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ContextProcessor:

    def __init__(self, address, port, organization_name, uname, psswd):
        super().__init__()
        try:
            if uname is not None:
                __mongo_client = MongoClient(address, port, username=uname, password=psswd)
            else:
                __mongo_client = MongoClient(address, port)
            __db = __mongo_client[f"repo_{organization_name}"]
            self.__collection  = __db["availableContext"]
        except Exception as e:
            print(f"{bcolors.FAIL}{e}")

    def message_return(self, value, context_name = None, exception = None):
        if value == 0:
            return f"{bcolors.FAIL}The context '{context_name}' is already present"
        elif value == 1:
            return f"{bcolors.OKGREEN}Successfully created the context {context_name}"
        elif value == 2:
            return f"{bcolors.FAIL}The context '{context_name}' you're trying to delete is not present"
        elif value == 3:
            return f"{bcolors.OKGREEN}Successfully deleted the context {context_name}"
        else:
            return f"{bcolors.FAIL}Unexpected error occured, while trying to process your request! Please try again. Exception: {exception}"

    def create_context(self, context_name):
        data = {
            "context_name" : context_name
        }

        try:
            if self.__collection.find({"context_name":context_name}).count() >= 1:
                status = 0
                return status, self.message_return(0, context_name=context_name)
            else:
                self.__collection.insert_one(data)
                status = 1
                return status, self.message_return(1, context_name=context_name)

        except Exception as e:
            return 0, self.message_return(5, exception=e)

    def delete_context(self, context_name):
 
        try:
            if self.__collection.find({"context_name":context_name}).count() == 1:
                result = self.__collection.delete_one({"context_name":context_name})
                status = 1
                return status, self.message_return(3, context_name=context_name)
            else:
                status = 0
                return status, self.message_return(2, context_name=context_name)               

        except Exception as e:
            return 0, self.message_return(5, exception=e)