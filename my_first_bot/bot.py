'''
MyFirstBot#9854
'''

import asyncio

import discord
from discord import Activity, ActivityType
from discord.ext.commands import Bot, Context, when_mentioned_or
from discord.ext.commands.errors import CheckFailure
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS

from cogs import OthersGog, GamesCog
from helpcmd import MyHelpCommand
from constants import BOT_TOKEN, CHANNELS_NAMES, COMMAND_PREFIX

class MyFirstBot(Bot):
    def __init__(self, *args, **kwargs):
        # make token a field to be accessible without reloading env
        self.TOKEN = BOT_TOKEN

        # bot will respond when mentioned and to a command prefix
        command_prefix = when_mentioned_or(COMMAND_PREFIX)
        # custom help command
        help_command = MyHelpCommand()
        # instantiate bot from parent class
        super().__init__(command_prefix, help_command=help_command, *args, **kwargs)

        # register cogs (commands)
        self.add_cog(OthersGog(self))
        self.add_cog(GamesCog(self))

    async def on_ready(self):
        # listening to
        activity = Activity(name='mentions or .help', type=ActivityType.listening)
        await self.change_presence(activity=activity)
        print(f'Logged in as {self.user}')

    async def on_command_error(self, context: Context, error):
        print(f'\tError: {error}')
        # if a member doesn't have permission to use a command
        if isinstance(error, CheckFailure):
            pensive = EMOJIS[':pensive:']
            text = f"Sorry {context.message.author.mention}, you don't have permission to use this command {pensive}"
            await context.send(text)

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
