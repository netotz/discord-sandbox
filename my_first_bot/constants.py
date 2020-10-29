'''
Project constants.
'''

import os

import dotenv

# load environment variables from .env (not commited to git)
dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNELS_NAMES = os.getenv('CHANNELS_NAMES').split()

#: Prefix for bot commands
COMMAND_PREFIX = '.'
