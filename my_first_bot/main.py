'''
MyFirstBot#9854
'''

import os

import discord
import dotenv

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged as {self.user}')

    async def on_message(self, message):
        if message.content.startswith('hey!'):
            await message.channel.send(f'Hey @{message.author}!')

# bot token is on a .env file, not commited to git
dotenv.load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

MyClient().run(TOKEN)
