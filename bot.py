import settings

class Tokenize(object):
    def __init__(self, data, addressed, ident):
        """
        A slimmed down version of Tokenizer.Data. data should be an re.match of
        a PRIVMSG
        """
        self.addressed = addressed
        self.ident = ident

        self.nick = data.group(1)
        self.username = data.group(2)
        self.host = data.group(3)
        self.channel = data.group(5)
        self.message = data.group(6)

        if self.channel.find("#") != -1:
            self.reply_to = channel
        else:
            self.reply_to = nick

    def has_key(self, key):
        """
        Returns True if self.message has key
        sets self.args to the string following key.
        """
        if not self.addressed:
            key = settings.COMMAND_TOKEN + key #Want to get rid of this and not have settings in this modules.

        f = self.message.find(key)
        if f != -1:
            self.args = self.message[f+len(key)+1:]
            return True
        

class Bot(object):
    def __init__(self):
        self.messages = []
        self.masters = {}
        self.commands = self.get_commands()

    def get_commands(self):
        """
        This should import all the .py files in /plugins and run module.get_commands()
        for each one. module.get_commands() returns a list of functions that gets
        added to self.commands
        """
        pass
        


    def parse(self, sock, data):
        """
        Replacement for Tokenizer.Data. There's so much shared functionality
        between Bot and Tokenizer.Data that it makes more sense to have parsing
        incoming messages be a method of Bot rather than passing Bot over every
        message.
        """

        if re.search('^:(.+)!(.+)@(.+) (.+) (.+) :(.+)$', data):
            m = re.search('^:(.+)!(.+)@(.+) (.+) (.+) :(.+)$', data)
            
            if data.find(self.nicks[id(sock)]) != -1:
                addressed = True
            else:
                addressed = False
                
            try:
                self.masters[m.group(3)] #host
                ident = True
            except:
                ident = False
                
            data = Tokenize(m, addressed, ident)

            #Here we run the commands.


        elif re.search('^PING :(.*)$', self.raw_data):
            sock.send('PONG')

        #We aren't really doing anything with these last two but I'll keep them in.
        elif re.search('^:(.+) ([0-9]+) (.+)$', self.raw_data):
            m = re.search('^:(.+) ([0-9]+) (.+)$', self.raw_data)
            self.host = m.group(1)
            self.type = 'SERVMSG'
            self.code = m.group(2)
            self.message = m.group(3)

        else:
            self.type = 'OTHER'

bot = Bot()
