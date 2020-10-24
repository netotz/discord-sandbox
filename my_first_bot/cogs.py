'''
Cogs for MyFirstBot
'''

import random
from dataclasses import dataclass
from typing import Tuple

from discord.ext import commands
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS

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
        text = f'{greeting} {ctx.message.author.mention}! {greet_emoji}'
        await ctx.send(text)

    @commands.command(
        name='heart-me',
        help=f'The bot reacts to your message with {EMOJIS[":heart:"]}')
    # only works if user has 'pro crack' role.
    @commands.has_role('pro crack')
    async def heart_me(self, ctx):
        heart = EMOJIS[':heart:']
        await ctx.message.add_reaction(heart)

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

        text = f"It's {face}, {phrase}"
        # save sent message
        message = await ctx.send(text)

        emoji = EMOJIS[':white_check_mark:'] if did_user_win else EMOJIS[':x:']
        try:
            # react with emoji to sent message
            await message.add_reaction(emoji)
        except Exception as exception:
            print(exception)
