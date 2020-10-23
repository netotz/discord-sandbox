'''
Run MyFirstBot.
'''

from bot import MyFirstBot

bot = MyFirstBot()

# run method in background
# bot.loop.create_task(bot.count_in_background())

bot.run(bot.TOKEN)
