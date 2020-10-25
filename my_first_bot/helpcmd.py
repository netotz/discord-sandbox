
from discord import Embed, Colour
from discord.ext.commands import HelpCommand, Context, Command
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS

class HelpEmbed(Embed):
    def __init__(self, context: Context):
        questionmark = EMOJIS[':grey_question:']
        super().__init__(
            title=f'{questionmark} Help',
            description="I'm a learning bot. These are my commands:",
            colour=Colour.red(),
            url='https://github.com/netotz/discord-sandbox'
        )

        self.set_thumbnail(url='http://iconbug.com/data/26/256/a2ccff2488d35d8ebc6189ea693cb4a0.png')
        self.set_footer(text='Page 1')

        command: Command
        for command in context.bot.commands:
            if command.hidden:
                continue
            self.add_field(
                name=command.name,
                value=command.help,
                inline=False
            )

class MyHelpCommand(HelpCommand):
    async def send_bot_help(self, mapping):
        ctx: Context = self.context

        embed = HelpEmbed(ctx)

        await ctx.send(embed=embed)
