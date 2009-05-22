"""
This is the core and main module. The majority of the functionality of the bot
should be imported from other modules to keep things easy to hotswap.
"""
import socket

import commands
import tokenizer
import settings

class Bot(object):
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commands = commands.get_commands()

    def connect(self):
        self.socket.connect((settings.HOST, settings.PORT))
        self.socket.send("NICK %s\r\n" % (settings.BOTNAME,))
        self.socket.send("USER %s\r\n" % (settings.BOTUSER,))

        if settings.AUTOJOIN:
            for channel in settings.CHANNELS:
                self.socket.send("JOIN %s %s\r\n" % (channel[0],channel[1]))

        if settings.GREETING:
            for channel in settings.CHANNELS:
                self.socket.send("PRIVMSG %s :%s\r\n" % (channel[0], settings.GREETING))
        
        while True:
            self.data = self.socket.recv(4096)
            tokenizer.Data(self)

    def reload(self):
        reload(commands)
        reload(tokenizer)
        reload(settings)
        self.commands = commands.get_commands()
        
if __name__ == '__main__':
    bot = Bot()
    bot.connect()