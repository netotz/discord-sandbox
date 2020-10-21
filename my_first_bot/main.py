'''
MyFirstBot#9854
'''

import os

from discord.ext import commands
import dotenv

class MyFirstBot(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

class Greeting(commands.Cog):
    @commands.command()
    async def hey(self, ctx):
        '''
        Returns the greeting :)
        '''
        await ctx.send(f'Hey {ctx.message.author}!')

# bot token is in a .env file, not commited to git
dotenv.load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# bot will respond when mentioned rather to a command prefix
bot = MyFirstBot(commands.when_mentioned)
# register cog (commands)
bot.add_cog(Greeting(bot))
bot.run(TOKEN)
