'''
MyFirstBot#9854
'''

import os
import asyncio
import random
from dataclasses import dataclass
from typing import Tuple

import discord
from discord.ext import commands
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS
import dotenv

# load environment variables from .env (not commited to git)
dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNELS_NAMES = os.getenv('CHANNELS_NAMES').split()

@dataclass
class OthersGog(commands.Cog):
    bot: commands.Bot
    greetings: Tuple[str, ...] = (
        'Hey',
        'Hi',
        'Hello',
        'Hola',
        'Saludos',
        'Saluton',
    )
    greet_emojis: Tuple[str, ...] = tuple(
        EMOJIS[alias] for alias in (
            ':grinning:',
            ':smiley:',
            ':smile:',
            ':grin:',
            ':relaxed:',
            ':blush:',
            ':wink:',
            ':yum:',
        )
    )

    @commands.command(help='Greet the bot!')
    async def hey(self, ctx):
        '''
        Returns a random greeting with a random emoji.
        '''
        greeting = random.choice(self.greetings)
        greet_emoji = random.choice(self.greet_emojis)
        await ctx.send(f'{greeting} {ctx.message.author.mention}! {greet_emoji}')

    @commands.command(
        name='heart-me',
        help=f'The bot reacts to your message with {EMOJIS[":heart:"]}')
    # only works if user has 'pro crack' role.
    @commands.has_role('pro crack')
    async def heart_me(self, ctx):
        await ctx.message.add_reaction(EMOJIS[':heart:'])

    def __hash__(self):
        '''
        Override to allow class to have tuple fields.
        '''
        return id(self)

class GamesCog(commands.Cog):
    @commands.command(
        help='Play heads or tails, choose your face: type "toss heads" or "toss tails"'
    )
    async def toss(self, ctx, userface: str):
        '''
        Play heads or tails.
        '''
        # heads is True, tails is False
        tossed = random.random() <= 0.5
        did_user_win = tossed == (userface == 'heads')

        phrase = 'you won...' if did_user_win else 'YOU LOST!!!'
        face = 'heads' if tossed else 'tails'
        # save sent message
        message = await ctx.send(f"It's {face}, {phrase}")

        emoji = EMOJIS[':white_check_mark:'] if did_user_win else EMOJIS[':x:']
        try:
            # react with emoji to sent message
            await message.add_reaction(emoji)
        except Exception as exception:
            print(exception)

class MyFirstBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        # make token a field to be accessible without reloading env
        self.TOKEN = BOT_TOKEN

        # bot will respond when mentioned rather to a command prefix
        command_prefix = commands.when_mentioned
        # instantiate bot core from parent class
        super().__init__(command_prefix, *args, **kwargs)

        # register cogs (commands)
        self.add_cog(OthersGog(self))
        self.add_cog(GamesCog(self))

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_command_error(self, ctx, error):
        # if a member doesn't have permission to use a command
        if isinstance(error, commands.errors.CheckFailure):
            pensive = EMOJIS[':pensive:']
            await ctx.send(f"Sorry {ctx.message.author.mention}, you don't have permission to use this command {pensive}")

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
                await channel.send(f'{counter} minutes')

            await asyncio.sleep(seconds)
            counter += seconds / 60
