import settings
import re

class Data(object):
    def __init__(self, bot):
        self.bot = bot
        self.raw_data = bot.socket.recv(4096)
        print self.raw_data

        if re.search('^:(.+)!(.+)@(.+) (.+) (.+) :(.+)$', self.raw_data):
            m = re.search('^:(.+)!(.+)@(.+) (.+) (.+) :(.+)$', self.raw_data)
            self.nick = m.group(1)
            self.username = m.group(2)
            self.host = m.group(3)
            self.type = m.group(4)
            self.channel = m.group(5)
            self.message = m.group(6)
            self.args = None

            if self.raw_data.find(settings.BOTNAME) != -1:
                self.addressed = True
            else:
                self.addressed = False

            try:
                settings.MASTERS[self.host]
                self.ident = True
            except:
                self.ident = False

            if self.channel.find("#") != -1:
                self.reply_to = self.channel
            else:
                self.reply_to = self.nick

            for command in bot.commands:
                command(self)

        elif re.search('^PING :(.*)$', self.raw_data):
            m = re.search('^PING :(.*)$', self.raw_data)
            self.host = m.group(1)
            self.type = 'PING'
            self.send('PONG')

        elif re.search('^:(.+) ([0-9]+) (.+)$', self.raw_data):
            m = re.search('^:(.+) ([0-9]+) (.+)$', self.raw_data)
            self.host = m.group(1)
            self.type = 'SERVMSG'
            self.code = m.group(2)
            self.message = m.group(3)

        else:
            self.type = 'OTHER'

    def __repr__(self):
        return self.raw_data

    def has_key(self, key):
        """
        Returns True if self.message has key
        sets self.args to the string following key.
        """
        if not self.addressed:
            key = settings.COMMAND_TOKEN + key

        f = self.message.find(key)
        if f != -1:
            self.args = self.message[f+len(key)+1:]
            return True

    def send(self, message):
        self.bot.socket.send(message)
        print '>>> %s' % message

    def reply(self, text):
        self.send("PRIVMSG %s :%s\r\n" % (self.reply_to, text))