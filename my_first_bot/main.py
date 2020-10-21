'''
MyFirstBot#9854
'''

import os

import discord
import dotenv

def init_client():
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'Logged as {client.user}')

    @client.event
    async def on_message(message):
        if message.content.startswith('hey!'):
            await message.channel.send(f'Hey @{message.author}!')

    return client

# bot token is on a .env file, not commited to git
dotenv.load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

init_client().run(TOKEN)
