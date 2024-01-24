import logging
from logging import FileHandler, StreamHandler

def setup_logger( log_file: str="" ):
    """
    Function that sets up a logger.

    Args:
        log_file (str, optional): If wanted, add a log file. Defaults to "".
    """
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s", datefmt="%m-%d-%y %H:%M:%S")

    # Create a file handler and set the level to INFO
    if log_file:
        file_handler = FileHandler( log_file )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter( logging.Formatter( "%(asctime)s - %(name)s - %(message)s", datefmt="%m-%d-%y %H:%M:%S" ) )
        logger.addHandler(file_handler)

    # Create a console handler and set the level to INFO
    console_handler = StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter( logging.Formatter( "%(message)s" ) )
    logger.addHandler(console_handler)

    # Set the level of thid-party logger to avoid dumping too much information
    for log_ in ['markdown_it', 'h5py', 'numexpr', 'git']: 
        logging.getLogger(log_).setLevel('WARNING')