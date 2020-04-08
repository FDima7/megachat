# Server ver 1.0
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

        data = data.decode() #encoding='utf8'

        if self.loginuser is not None:
            self.send_message(data)
        else:
            if data.startswith('#'):
                data.replace('#', '')
                self.loginuser = (2)
                self.transport.write(f"Привет, {self.loginuser}!\n".encode(encoding='utf-8'))
            else:
                self.transport.write("Неправильный логин".encode())
        print(str(datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")) + ' - ' + str(self.loginuser) + data)

    def send_message(self, content: str):
        message = f"{self.loginuser}: {content}\n"

        for user in self.server.users:
            user.transport.write(message.encode())

    def connection_lost(self, exception):
        self.server.users.remove(self)
        print(str(datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")) + ' - ' + "Клиент покинул чат")

    def connection_made(self, transport: transports.Transport):
        self.server.users.append(self)
        self.transport = transport
        print(str(datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")) + ' - ' + "Подключен неавторизированный пользователь")


class ServerSetting:
    users: list

    def __init__(self):
        self.users = []  # Пустой список клиентов при запуске

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


