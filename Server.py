# Server ver 1.001
# FDima7
#

import asyncio
from asyncio import transports
import datetime


class ServerWorking(asyncio.Protocol):
    loginuser: str = None
    server: 'ServerSetting'
    transport: transports.Transport

    def __init__(self, server: 'ServerSetting'):
        self.server = server

    def data_received(self, data: bytes):
        data = data.decode()  # encoding='utf8'

        if self.loginuser is not None:
            self.send_message(data)
        else:
            if data.startswith('#'):
                data = data.replace('#', '')
                n = 0
                for user in self.server.users:
                    if user == str(data):
                        n = n + 1
                        if n > 1:
                            self.transport.write('Sorry, but your login is busy - active'.encode('utf-8'))
                            self.transport.close()
                    else:
                        self.server.users.append(data)

                self.loginuser = data
                print(self.loginuser)
                self.transport.write(f"Welcome, {self.loginuser}!\n".encode('utf-8'))
                n = -9
                while n < -0:
                    try:
                        while n < -0:
                            self.server.history_new.append(self.server.history[n])
                            n = n + 1
                    except IndexError:
                        n = n + 1
                #print(self.server.history_new)
                history10 = self.server.history_new
                self.transport.write(f"{history10}".encode('utf-8'))

            else:
                self.transport.write("Pls, Login in\n".encode('utf-8'))
                self.transport.write("You are disconnected".encode('utf-8'))
                self.transport.close()

        print(str(datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")) + ' - ' + str(self.loginuser) + ' написал ' + data)  # Лог работы софта

    def send_history(self, message: str):
        print(message)
        self.server.history.append(message)

    def send_message(self, content: str):
        message = f"{self.loginuser} post: {content}\n"
        self.send_history(message.replace('b', "").replace('\n', ""))
        for user in self.server.users:
            if user != self.loginuser:
                user.transport.write(message.encode())

    def connection_lost(self, exception):
        self.server.users.remove(self)
        self.transport.close()
        self.server.users.remove(self.loginuser)
        print(str(datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")) + ' - ' + "Клиент покинул чат")

    def connection_made(self, transport: transports.Transport):
        self.server.users.append(self)
        self.transport = transport
        print(str(datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")) + ' - ' + "Подключение пользователя")


class ServerSetting:
    users: list
    history = []
    history_new = []

    def __init__(self):
        self.users = []  # Пустой список клиентов при запуске
        print(self.users)

    def build_protocol(self):
        return ServerWorking(self)

    async def start(self):
        ip = '127.0.0.1'
        port = 6666
        working = asyncio.get_running_loop()
        coroutine = await working.create_server(self.build_protocol, ip, port)
        print(str(datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")) + ' - ' 'Сервер успешно запущен с адресса ' + str(ip) + ':' + str(port))
        await coroutine.serve_forever()

process = ServerSetting()

try:
    asyncio.run(process.start())
except KeyboardInterrupt:
    print('Сервер временно не доступен')
#except Exception:
    #print('Выполняются технические работы')
