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
import dotenv

# bot token is in a .env file, not commited to git
dotenv.load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD_NAME = os.getenv('GUILD_NAME')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')

@dataclass
class GreetingsCog(commands.Cog):
    bot: commands.Bot
    greetings: Tuple[str, ...] = ('Hey', 'Hello', 'Hola', 'Saludos', 'Saluton')

    @commands.command()
    async def hey(self, ctx):
        '''
        Returns a greeting :)
        '''
        greeting = random.choice(self.greetings)
        await ctx.send(f'{greeting} {ctx.message.author.name}!')

class GamesCog(commands.Cog):
    @commands.command()
    async def coin(self, ctx, userface: str):
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

        emoji = '\N{WHITE HEAVY CHECK MARK}' if did_user_win else '\N{CROSS MARK}'
        try:
            # react with emoji to sent message
            await message.add_reaction(emoji)
        except Exception as exception:
            print(exception)

class MyFirstBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        # bot will respond when mentioned rather to a command prefix
        super().__init__(commands.when_mentioned, *args, **kwargs)
        # register cogs (commands)
        self.add_cog(GreetingsCog(self))
        self.add_cog(GamesCog(self))

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def count_in_background(self, step=60):
        '''
        Counts minutes in background.
        '''
        await self.wait_until_ready()

        guild = discord.utils.get(self.guilds, name=GUILD_NAME)
        channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)

        counter = 0
        while not self.is_closed():
            await asyncio.sleep(step)

            counter += step / 60
            await channel.send(f'{counter} m')

bot = MyFirstBot()

# run method in background
# bot.loop.create_task(bot.count_in_background())

bot.run(TOKEN)
