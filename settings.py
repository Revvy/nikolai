HOST = 'irc.adelais.net'
PORT = 6667
BOTNAME = 'hurrdurr'
BOTUSER = 'py py py py py bot'

MASTERS = {}
PASSWORD = 'password'


# (channel name, password [optional])
CHANNELS = [
	('#omgabot', ''),
	]

AUTOJOIN = True
GREETING = 'hurr'

# All relevant commands that you want processed should start with this string
# Contained within the commands module
# Yea, MUDs and all that.  I've been a nerd for a while
COMMAND_PREFIX = 'do_'
COMMAND_TOKEN = '@'

# Local settings override
try:
    from local_settings import *
except ImportError:
    pass


