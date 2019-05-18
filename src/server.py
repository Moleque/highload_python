# import asyncio
import socket
import multiprocessing

from worker import Worker

CONNECTIONS_COUNT = 1024

class Server:

    def __init__(self, ip, port, rootDir, threadsCount):
        # конфигурирование сокета
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen(CONNECTIONS_COUNT)
        sock.setblocking(False)

        # создание воркеров для обработки запросов
        workers = []
        for _ in range(threadsCount):
            process = multiprocessing.Process(target = Worker, args = (sock, rootDir))
            workers.append(process)
            process.start()
        
        # завершение работы воркеров сервера
        try:
            for process in workers:
                process.join()
        except KeyboardInterrupt:
            for process in workers:
                process.terminate()

        print('server stoped')
