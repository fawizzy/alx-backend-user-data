import re
from typing import List
import logging

def filter_datum(fields: List[str], redaction: str, message: str, seperator: str):
    pattern = re.compile("")
    for field in fields:
        pattern = re.compile(field + "=.*?" + seperator)
        message = re.sub(pattern,"hello", message)
              #message = re.sub(field, redaction, message)
    
    return message

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields
    def format(self,record: logging.LogRecord) -> str:
        message = record
        for field in self.fields:
            print(message)
            message = filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)
        return message