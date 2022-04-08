import discord
import asyncio
import random
from game_classes import tictactoe
from discord.ext import commands
from asyncio.exceptions import TimeoutError

class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ttt')
    async def tictactoe(self, ctx, player2: discord.Member=None):
        """Starts a tic tac toe game with a specified second player."""
        if not player2:
            await ctx.send(f"{ctx.author.mention} You must specify a second player")
            return
        try:
            tictactoe_session = tictactoe.TicTacToe(ctx.author, player2) # Creates a tic tac toe game
        except Exception:
            await ctx.send(f"{ctx.author.mention} you cannot play against yourself.", delete_after=3.0)
            return  
        game_embed = discord.Embed(title=':x: TIC TAC TOE :o:',
                                   description=f"""
                                   Player 1: {tictactoe_session.player1['User'].mention} {tictactoe_session.player1['Piece']}
                                   Player 2: {tictactoe_session.player2['User'].mention} {tictactoe_session.player2['Piece']}

                                   {tictactoe_session.display_board()}""" )

        # Sends the first initial messages that are to edited in the main game loop
        turn_indicator_message = await ctx.send(f"{tictactoe_session.active_player['User'].mention} It's your turn!")
        tictactoe_embed = await ctx.send(embed=game_embed)

        tries = 9 # Since there are only 9 tiles on a tic tac toe board, it makes sense that both players should have only that many tries in total.
        is_tie = True # Triggers an if statement outside of the game loop. If a player wins or a TimeoutError is raised, this value will be changed to False.
        # Main game loop
        while tries > 0:
            game_embed = discord.Embed(title=':x: TIC TAC TOE :o:',
                                description=f"""
                                Player 1: {tictactoe_session.player1['User'].mention} {tictactoe_session.player1['Piece']}
                                Player 2: {tictactoe_session.player2['User'].mention} {tictactoe_session.player2['Piece']}

                                {tictactoe_session.display_board()}""" ) 

            # I chose to edit messages instead of sending them over again because I personally feel that it is more well-suited for a tic tac toe game.
            await turn_indicator_message.edit(content=f"{tictactoe_session.active_player['User'].mention} It's your turn!")
            await tictactoe_embed.edit(embed=game_embed)
            try:
                # Waits for user input and makes sure that the message it reads in as input is from the active player. They have 60 seconds to enter their input before a TimeoutError is raised. 
                spot = await self.bot.wait_for("message", timeout=60, check=lambda message: message.author == tictactoe_session.active_player['User'] and message.content in ['1', '2', '3', '4', '5', '6', '7', '8', '9']) # I chose to do strings for the numbers over integers because by default, spot.content is a string.

            except TimeoutError: # If the player is AFK for too long or simply does not care to play the game
                is_tie = False
                await turn_indicator_message.delete() 
                timeout_embed = discord.Embed(title="TIC TAC TOE", description=f"Player1: {tictactoe_session.player1['User'].mention}\nPlayer2: {tictactoe_session.player2['User'].mention}\n\nThis game was not completed because one of the players stopped responding.")
                await tictactoe_embed.edit(embed=timeout_embed)
                break 

            try:
                tictactoe_session.modify_board(int(spot.content)) # spot.content because that's the actual content of the message. Just putting spot just returns the object
            except Exception: # Test how this works another time. 
                original_message_content = turn_indicator_message.content # Will be used to revert the content back to that of the old after the 3 second sleep. 
                await turn_indicator_message.edit(content=f"{tictactoe_session.active_player['User'].mention} that spot is taken!")
                await asyncio.sleep(0.5)
                await turn_indicator_message.edit(content=original_message_content)
                continue # Stops the active player from being changed


            has_won = tictactoe_session.check_wins() # This method returns True if a win has been detected
            if has_won:
                is_tie = False
                await turn_indicator_message.delete()
                winning_embed = discord.Embed(title='TIC TAC TOE', description=f'Winner: :medal: {tictactoe_session.active_player["User"].mention}')
                await tictactoe_embed.edit(embed=winning_embed)
                break
            tictactoe_session.change_active_player()
            tries -= 1

        if is_tie:
            tie_embed = discord.Embed(title='TIC TAC TOE', description=f"Tied game between {tictactoe_session.player1['User'].mention} and {tictactoe_session.player2['User'].mention}")
            await tictactoe_embed.edit(embed=tie_embed)
    
    @commands.command(name="diceroll")
    async def dice_roll(self, ctx):
        dice_rolled = random.randint(1, 6)
        await ctx.send(f":game_die: {ctx.author.mention} you rolled {dice_rolled} :game_die:")

    @commands.command(name="coinflip")
    async def coin_flip(self, ctx):
        coin_side = random.choice(['Heads', "Tails"])
        await ctx.send(f":coin: {ctx.author.mention} you got {coin_side} :coin:")

        

def setup(bot: commands.Bot):
    bot.add_cog(GameCommands(bot))
