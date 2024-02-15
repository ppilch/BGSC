import inspect

class Helpers:
    
    def replace_quotes(self, input_string):
        print(inspect.currentframe().f_code.co_name)
        return input_string.replace("'","''")
        