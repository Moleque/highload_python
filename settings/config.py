import os
import re

fields = {
    'cpu_limit' : re.compile(r'cpu_limit\s+(?P<cpu_limit>\d+)'),
    'thread_limit' : re.compile(r'thread_limit\s+(?P<thread_limit>\d+)'),
    'document_root' : re.compile(r'document_root\s+(?P<document_root>[^\s]+)'),
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
                match = fields[field].search(content)
                if match:
                    if field == 'cpu_limit':
                        self.cpu = int(match.group(field))
                    elif field == 'thread_limit':
                        self.thread = int(match.group(field))
                    elif field == 'document_root':
                        self.root = match.group(field)
        return True
