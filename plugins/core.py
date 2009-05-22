import urllib
try:
   import simplejson as json
except:
    print 'Failed to import simplejson'

command_prefix = 'do_'

def get_commands():
    return [v for k,v in globals().items() if k.startswith(command_prefix)]

def do_ident(data):
    """
    Identified the user's host to the bot.
    """
    if data.has_key('ident'):
        if not data.ident:
            if data.args.find(settings.PASSWORD) != -1:
                settings.MASTERS[data.host] = 1
                data.reply('Successfully identified')
            else:
                data.reply('Incorrect password')
        else:
            data.reply('Already identified')

def do_reload(data):
    """
    Forces the bot to reload commands.py.
    """
    if data.has_key('reload'):
        if data.ident:
            data.bot.reload()
            data.reply('Bot reloaded')
        else:
            data.reply('You are not authorized to preform that operation')

def do_google(data):
    if data.has_key('google'):
        if data.args:
            url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%(term)s" % { 'term' : urllib.quote(data.args) }
            response = json.load(urllib.urlopen(url))
            data.reply("Total Results: %(total)s" % { 'total' : response['responseData']['cursor']['estimatedResultCount'] })
            data.reply(response['responseData']['results'][0]['url'])
        else:
            pass

def do_hello(data):
    if data.has_key('hello'):
        data.reply('Sup, %s.' % data.nick)

def do_help(data):
    """
Provides a list of commands or help for a specific command
[ if you don't want to incur runtime errors, keep this function at the bottom of the module ]
"""
    if data.has_key('help'):
        if data.args:
            pass
        else:
            bot._msg(data.reply, "List of commands:")

            for k,v in globals().items():
                if k.startswith(settings.COMMAND_PREFIX):
                    bot._msg(data.reply, "%s: %s" % (k[3:], v.__doc__))
