'''
Custom help command.
'''

from typing import List

from discord import Embed, Colour
from discord.ext.commands import HelpCommand, Context, Command
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS
from disputils import BotEmbedPaginator

def get_command_params(command: Command) -> str:
    OMIT_PARAMS = ('self', 'ctx', 'context')
    params = ''.join(
        f' [{param}]'
        for param in command.params
        if param not in OMIT_PARAMS
    )
    return command.name + params

def create_help_embed(commands: List[Command]):
    questionmark = EMOJIS[':grey_question:']
    embed = Embed(
        title=f'{questionmark} About the bot',
        description="I'm a learning bot. You can mention me or use prefix `.`\nThese are my commands:",
        colour=Colour.red(),
        url='https://github.com/netotz/discord-sandbox'
    )

    embed.set_thumbnail(url='http://iconbug.com/data/26/256/a2ccff2488d35d8ebc6189ea693cb4a0.png')

    for command in commands:
        embed.add_field(
            name=get_command_params(command),
            value=command.help,
            inline=False
        )

    return embed

def create_command_embed(command: Command):
    fullcommand = get_command_params(command)
    docstring = command.callback.__doc__ or ''
    description = f'{command.help}\n{docstring}'
    embed = Embed(
        title=f'`{fullcommand}`',
        description=description,
        colour=Colour.default()
    )

    questionmark = EMOJIS[':grey_question:']
    embed.set_author(
        name=f'{questionmark} Command help'
    )

    return embed

def create_help_paginator(context: Context, n: int):
    commands = [command for command in context.bot.commands if not command.hidden]
    embeds = [create_help_embed(commands[i:i+n]) for i in range(0, len(commands), n)]
    return BotEmbedPaginator(context, embeds)

class MyHelpCommand(HelpCommand):
    def __init__(self, **options):
        # change default help message for help command
        attrs = {'help': 'Shows this message, or get help of a specified command.'}
        super().__init__(command_attrs=attrs, **options)

    async def send_bot_help(self, mapping):
        paginator = create_help_paginator(self.context, 6)
        await paginator.run()

    async def send_command_help(self, command: Command):
        embed = create_command_embed(command)
        await self.context.send(embed=embed)
