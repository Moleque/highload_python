import os
import re

__all__ = (
    'Config'
)

fields = {
    'cpu_limit' : {
        'pattern' : re.compile(r'cpu_limit\s+(?P<cpu_limit>\d+)'),
        'type'    : int,
    },
    'thread_limit' : {
        'pattern' : re.compile(r'thread_limit\s+(?P<thread_limit>\d+)'),
        'type'    : int,
    },
    'document_root' : {
        'pattern' : re.compile(r'document_root\s+(?P<document_root>[^\s]+)'),
        'type'    : str,
    },
}


class Settings:

    def __init__(self):
        self.cpu = 4
        self.thread = 256
        self.root = '/var/www/html'

    #  парсинг конфигурационного файла
    def parseConfig(self, path):
        if not(os.path.exists(path)):  
            return False

        with open(path, 'r') as file:
            content = file.read()

            for field in fields:
                param = fields[field]
                match = param['pattern'].search(content)
                if match:
                    if field == 'cpu_limit':
                        self.cpu = match.group(field)
                    elif field == 'thread_limit':
                        self.thread = match.group(field)
                    elif field == 'document_root':
                        self.root = match.group(field)
        return True
