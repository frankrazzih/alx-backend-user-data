#!/usr/bin/env python3
'''format logs using regex'''
import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str)->str:
    '''filter a log message'''
    #search for the field pattern in the message
    for field in fields:
        pat = re.compile(f'{field}=(.*?){separator}')
        match = pat.search(message)
        if match:
            message = re.sub(match.group(1), redaction, message)
    return message

import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
        record = super().format(record)
        record = str(record)
        message = filter_datum(self.fields, self.REDACTION, record, self.SEPARATOR)
        return message
