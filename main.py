'''
Purpose: A discord bot that allows server members to play games by themselves or with one another. 
Creation Date: 17/10/2021
'''

import discord
import specifications
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True 

bot = commands.Bot(command_prefix=specifications.prefix)

bot.remove_command("help")

@bot.command(name="help")
async def help(ctx):
    help_embed = discord.Embed(title="Game commands", description=f"`{specifications.prefix}ttt <@player2>`\nStarts a Tic Tac Toe game with a specified second player.\n\n`{specifications.prefix}coinflip`\nFlips a coin.\n\n`{specifications.prefix}diceroll`\nRolls a die.")
    emoji = "✅"
    await ctx.message.add_reaction(emoji)
    await ctx.author.send(embed=help_embed)


bot.load_extension('games')
bot.load_extension('command_logging')
bot.run('BOT TOKEN')
