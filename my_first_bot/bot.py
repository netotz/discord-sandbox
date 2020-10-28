'''
MyFirstBot#9854
'''

import os
import asyncio

import discord
from discord.ext.commands import Bot, when_mentioned
from discord.ext.commands.errors import CheckFailure
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS
import dotenv

from cogs import OthersGog, GamesCog
from helpcmd import MyHelpCommand

# load environment variables from .env (not commited to git)
dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNELS_NAMES = os.getenv('CHANNELS_NAMES').split()

class MyFirstBot(Bot):
    def __init__(self, *args, **kwargs):
        # make token a field to be accessible without reloading env
        self.TOKEN = BOT_TOKEN

        # bot will respond when mentioned rather to a command prefix
        command_prefix = when_mentioned
        help_command = MyHelpCommand()
        # custom help command
        # instantiate bot core from parent class
        super().__init__(command_prefix, help_command=help_command, *args, **kwargs)

        # register cogs (commands)
        self.add_cog(OthersGog(self))
        self.add_cog(GamesCog(self))

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_command_error(self, ctx, error):
        print(f'\tError: {error}')
        # if a member doesn't have permission to use a command
        if isinstance(error, CheckFailure):
            pensive = EMOJIS[':pensive:']
            text = f"Sorry {ctx.message.author.mention}, you don't have permission to use this command {pensive}"
            await ctx.send(text)

    async def count_in_background(self, seconds=60):
        '''
        Counts minutes in background.
        '''
        await self.wait_until_ready()

        # retrieve specified channels from .env
        channels = [
            discord.utils.get(guild.text_channels, name=channel_name)
            for guild, channel_name in zip(self.guilds, CHANNELS_NAMES)
        ]

        counter = 0
        while not self.is_closed():
            for channel in channels:
                text = f'{counter} minutes'
                await channel.send(text)

            await asyncio.sleep(seconds)
            counter += seconds / 60
