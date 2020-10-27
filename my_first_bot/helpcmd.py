
from discord import Embed, Colour
from discord.ext.commands import HelpCommand, Context, Command
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS

def create_help_embed(context: Context):
    questionmark = EMOJIS[':grey_question:']
    embed = Embed(
        title=f'{questionmark} Help',
        description="I'm a learning bot. These are my commands:",
        colour=Colour.red(),
        url='https://github.com/netotz/discord-sandbox'
    )

    embed.set_thumbnail(url='http://iconbug.com/data/26/256/a2ccff2488d35d8ebc6189ea693cb4a0.png')
    embed.set_footer(text='Page 1')

    command: Command
    for command in context.bot.commands:
        if command.hidden:
            continue
        embed.add_field(
            name=command.name,
            value=command.help,
            inline=False
        )

    return embed

class MyHelpCommand(HelpCommand):
    async def send_bot_help(self, mapping):
        ctx: Context = self.context

        embed = create_help_embed(ctx)

        await ctx.send(embed=embed)
