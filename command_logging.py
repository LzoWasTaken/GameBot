import discord
import specifications 
from discord.ext import commands 

class CommandLogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener(name="on_command")
    async def on_command(self, ctx):
        channel = self.bot.get_channel(specifications.logging_channel)
        # Creates an embed that will be sent into the log channel 
        logging_embed = discord.Embed(title="Command Log", description=f'{ctx.message.content}')
        logging_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        try:
            await channel.send(embed=logging_embed)
        except:
            pass

def setup(bot: commands.Bot):
    bot.add_cog(CommandLogging(bot))


