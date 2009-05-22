import socket, select

import bot
import settings

class NetworkInput:
    def __init__(self):
        self.sockets = []
        self.nicks = {} #Replace this with a get_nicks() method

    def connect(self):
        bot.connect()
        for network in settings.networks:
            sock = socket.socket()
            try:
                port = network['port']
            except:
                port = 6667
            sock.connect((network['host'], port))

            try:
                nick = network['nick']
            except:
                nick = settings.defaultNick
            sock.send('NICK %s\r\n' % nick)

            try:
                user = network['user']
            except:
                user = settings.defaultUser
            sock.send('USER %s\r\n' % user)
            #Should try altNick is user is in use.
            self.nicks[id(sock)] = user

            for channel in network['channels']:
                sock.send('JOIN %s %s\r\n' % (channel[0], channel[1]))

            self.sockets.append(sock)
        bot.bot.nicks = self.nicks

        while 1:
            read, write, exception = select.select(self.sockets,[],[])
            for sock in read:
                try:
                    data = network.recv(4096)
                    bot.bot.parse(sock, data)

                except:
                    print 'something went wrong'

    def reload(self):
        reload(bot)
        bot.bot.nicks = self.nicks #Replace this with a get_nicks() method

if __name__ == '__main__':
    networkInput = NetworkInput()
    networkInpuit.connect()