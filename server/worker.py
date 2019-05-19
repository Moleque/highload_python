import socket
import os
import asyncio
import uvloop

from datetime import datetime
from urllib.parse import unquote

import http.constants as constants
from http.request import Request 
from http.response import Response

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

CHUNK_SIZE = 262144

class Worker:

    def __init__(self, listenSocket, rootDir):#, config: conf.Config):
        self.listenSocket = listenSocket
        self.rootDir = rootDir

        self.parser = Request()
        
        self.loop = uvloop.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._run())

    async def _run(self):
        while True:
            handleSocket, _ = await self.loop.sock_accept(self.listenSocket)
            # connection.settimeout(5)
            self.loop.create_task(self.handle(handleSocket))

    async def _read(self, sock):
        return (await self.loop.sock_recv(sock, CHUNK_SIZE)).decode('utf8')

    async def _write(self, socket, response, file_path = None):
        await self.loop.sock_sendall(socket, str(response).encode('utf-8'))
        if file_path is not None and self.parser.method != 'HEAD':
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda : f.read(CHUNK_SIZE), b''):
                    await self.loop.sock_sendall(socket, chunk)

    async def handle(self, handleSocket):
        request = await self._read(handleSocket)
 
        if not self.parser.parse(request):
            await self._write(handleSocket, Response(400))
            handleSocket.close()
            return

        if self.parser.method not in constants.ALLOWED_METHODS:
            await self._write(handleSocket, Response(405))
            handleSocket.close()
            return

        #path не должен начинаться со /
        file_path = os.path.join(self.rootDir, self.parser.path)
        file_path = unquote(file_path)
        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            await self._write(handleSocket, Response(404))
            handleSocket.close()
            return

        dir_requested = False

        if os.path.isdir(file_path):
            dir_requested = True
            file_path = os.path.join(file_path, constants.INDEX_FILE)
            if not os.path.exists(file_path):
                await self._write(handleSocket, Response(403))
                handleSocket.close()
                return

        if os.path.isfile(file_path):
            if self.parser.path.endswith('/') and not dir_requested:
                await self._write(handleSocket, Response(404))
            else:
                mime_type, _ = mimetypes.guess_type(file_path)
                headers = {
                    'Content-Length': str(os.path.getsize(file_path)),
                    'Content-Type': mime_type,
                }
                await self._write(handleSocket, Response(200, headers_dict = headers), file_path)
            handleSocket.close()
            return