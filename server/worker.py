import socket
import os
import asyncio
import uvloop

from datetime import datetime
from urllib.parse import unquote

from server.parser import Http

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

CHUNK_SIZE = 256

class Worker:

    def __init__(self, listenSocket, rootDir):
        self.listenSocket = listenSocket
        self.rootDir = rootDir
        
        self.loop = uvloop.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._run())

    async def _run(self):
        while True:
            handleSocket, _ = await self.loop.sock_accept(self.listenSocket)
            self.loop.create_task(self.handle(handleSocket))

    async def _read(self, sock):
        return (await self.loop.sock_recv(sock, CHUNK_SIZE)).decode('utf8')

    async def _write(self, sock, response, filePath = None):
        await self.loop.sock_sendall(sock, str(response).encode('utf-8'))
        if filePath is not None:
            with open(filePath, 'rb') as file:
                for chunk in iter(lambda : file.read(CHUNK_SIZE), b''):
                    await self.loop.sock_sendall(sock, chunk)

    async def handle(self, handleSocket):
        query = await self._read(handleSocket)

        request = Http(query, self.rootDir)
        request.parse(query)
        response = request.get_response()

        filePath = None
        if request.Request['method'] != 'HEAD' and request.Response['status'] == 200:
            filePath = request.Request['filename']
        await self._write(handleSocket, response, filePath)
        
        handleSocket.close()
        return