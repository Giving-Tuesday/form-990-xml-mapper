import logging # Import Pythons Logging Library

# Error Log Location
access_log_location = '../Logs/access.log' 
error_log_location = '../Logs/error-generic.log' 
node_error_log_location = '../Logs/error-nodes.log' 
schema_error_log_location = '../Logs/error-schemas.log' 

## Create Simple Logging Class that will create & store script as a variable. 
class Error_Details:
    def __init__(
            self,
            script: str,
    ) -> None:
        self.script = script

    def get_detail_info(self):
        return {
            "script": self.script,
        }

##### Access Logger

## Create Error Logger
logger_access  = logging.getLogger("access")
logger_access.setLevel(logging.INFO)

## Setup Error Log Handler -> In this case a file handler to dump error log to /logs/error.log
access_file_handler =  logging.FileHandler(access_log_location, mode='a')

## Setup Error Log Formatter -> To ensure error logs have appropriate time stamps
access_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
access_file_handler.setFormatter(access_formatter)
logger_access.addHandler(access_file_handler)

## Create custom error log function that we can import anywhere in the code base
def log_access(e: Exception, message: str, detail: Error_Details):
    log = f"Script: {detail.script} - Message: {message}"
    logger_access.info(log)



##### Generic Error Logger

## Create Error Logger
logger_error  = logging.getLogger("error")
logger_error.setLevel(logging.ERROR)

## Setup Error Log Handler -> In this case a file handler to dump error log to /logs/error.log
error_file_handler =  logging.FileHandler(error_log_location, mode='a')

## Setup Error Log Formatter -> To ensure error logs have appropriate time stamps
error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
error_file_handler.setFormatter(error_formatter)
logger_error.addHandler(error_file_handler)

## Create custom error log function that we can import anywhere in the code base
def log_error(e: Exception, message: str, detail: Error_Details):
	log = f"Script: {detail.script} - Message: {message} - Details: {e}"
	logger_error.exception(log)


#### Node Error Logger

## Create Error Logger
logger_node_error  = logging.getLogger("nodes")
logger_node_error.setLevel(logging.ERROR)

## Setup Error Log Handler -> In this case a file handler to dump error log to /logs/error.log
error_node_file_handler =  logging.FileHandler(node_error_log_location, mode='a')

## Setup Error Log Formatter -> To ensure error logs have appropriate time stamps
error_node_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
error_node_file_handler.setFormatter(error_node_formatter)
logger_node_error.addHandler(error_node_file_handler)

## Create custom error log function that we can import anywhere in the code base
def log_node_error(e: Exception, message: str, detail: Error_Details):
    log = f"Script: {detail.script} - Message: {message} - Details: {e}"
    logger_node_error.error(log)


####### Schema Error Logger

## Create Error Logger
logger_schema_error  = logging.getLogger("schema")
logger_schema_error.setLevel(logging.ERROR)

## Setup Error Log Handler -> In this case a file handler to dump error log to /logs/error.log
schema_error_file_handler =  logging.FileHandler(schema_error_log_location, mode='a')

## Setup Error Log Formatter -> To ensure error logs have appropriate time stamps
schema_error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
schema_error_file_handler.setFormatter(schema_error_formatter)
logger_schema_error.addHandler(schema_error_file_handler)

## Create custom error log function that we can import anywhere in the code base
def log_schema_error(e: Exception, message: str, detail: Error_Details):
    log = f"Script: {detail.script} - Message: {message} - Details: {e}"
    logger_schema_error.exception(log)
