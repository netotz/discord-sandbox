'''
Custom help command.
'''

from typing import List

from discord import Embed, Colour
from discord.ext.commands import HelpCommand, Context, Command
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS
from disputils import BotEmbedPaginator

def create_help_embed(commands: List[Command]):
    questionmark = EMOJIS[':grey_question:']
    embed = Embed(
        title=f'{questionmark} Help',
        description="I'm a learning bot. These are my commands:",
        colour=Colour.red(),
        url='https://github.com/netotz/discord-sandbox'
    )

    embed.set_thumbnail(url='http://iconbug.com/data/26/256/a2ccff2488d35d8ebc6189ea693cb4a0.png')
    embed.set_footer(text='Page 1')

    for command in commands:
        omit_params = ('self', 'ctx', 'context')
        params = ''.join(f' [{param}]' for param in command.params if param not in omit_params)
        name = command.name + params
        embed.add_field(
            name=name,
            value=command.help,
            inline=False
        )

    return embed

def create_help_paginator(context: Context, n: int):
    commands = [command for command in context.bot.commands if not command.hidden]
    embeds = [create_help_embed(commands[i:i+n]) for i in range(0, len(commands), n)]
    return BotEmbedPaginator(context, embeds)

class MyHelpCommand(HelpCommand):
    async def send_bot_help(self, mapping):
        context: Context = self.context

        paginator = create_help_paginator(context, 2)
        await paginator.run()
