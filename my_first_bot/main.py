'''
MyFirstBot#9854
'''

import os
import asyncio

import discord
from discord.ext import commands
import dotenv

# bot token is in a .env file, not commited to git
dotenv.load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD_NAME = os.getenv('GUILD_NAME')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')

class MyFirstBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

            counter = step / 60
            await channel.send(f'{counter} m')

class Greeting(commands.Cog):
    @commands.command()
    async def hey(self, ctx):
        '''
        Returns the greeting :)
        '''
        await ctx.send(f'Hey {ctx.message.author}!')

# bot will respond when mentioned rather to a command prefix
bot = MyFirstBot(commands.when_mentioned)
# register cog (commands)
bot.add_cog(Greeting(bot))

# run method in background
# bot.loop.create_task(bot.count_in_background())

bot.run(TOKEN)
