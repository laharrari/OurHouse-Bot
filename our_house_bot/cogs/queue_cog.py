import discord
import asyncio
import random
from discord.ext import commands
from our_house_bot.our_house_bot import OurHouse

class QueueCog(commands.Cog, name = "queue"):
    def __init__(self, bot: OurHouse):
        super().__init__()
        
        self.bot = bot
        self.progress = False
        self.lobby = list()
        self.task = ""
        self.author = ""

    @commands.command(aliases=["commands"])
    async def help(self, ctx: commands.Context):
        msg = "Thank you for using OurHouse! It is still currently under development :)\n\n"
        msg += ".host - Start a lobby.\n"
        msg += ".lobby - See all participants in the lobby.\n"
        msg += ".random - Randomize everyone in the lobby to two teams.\n"
        msg += ".stop - Close the lobby.\n\n"
        msg += "If you have any questions or suggestions, please contact primal#7602! Thank you!"
        await ctx.send(msg)

    @commands.command()
    async def host(self, ctx: commands.Context):
        self.author = str(ctx.message.author)
        self.task = asyncio.create_task(self.preparePlayers(ctx))
        await self.task

    @commands.command()
    async def draft(self, ctx: commands.Context):
        await ctx.send("Draft Mode")

    @commands.command()
    async def randomdraft(self, ctx: commands.Context):
        await ctx.send("Random Draft Mode")

    @commands.command()
    async def pick(self, ctx: commands.Context):
        await ctx.send("Pick Player")

    @commands.command()
    async def random(self, ctx: commands.Context):
        await self.randomTeams(ctx)

    @commands.command()
    async def lobby(self, ctx: commands.Context):
        await self.printLobby(ctx)

    @commands.command()
    async def stop(self, ctx: commands.Context):
        await self.stopLobby(ctx)

    @commands.command()
    async def leave(self, ctx: commands.Context):
        if (ctx.message.author in lobby):
            self.lobby.remove(str(ctx.message.author))
            await ctx.send("{} has left the lobby.".format(ctx.message.author.name))
        else:
            await ctx.send("{} was not in the lobby.".format(ctx.message.author.name))

    async def preparePlayers(self, ctx: commands.Context):
        if (self.progress):
            await ctx.send("Lobby already in progress!")
        else:
            msg = await ctx.send("{} has started a lobby!\nAll participants click the ✅ to join. Type \".leave\" to leave.".format(ctx.message.author.name))
            await msg.add_reaction("✅")

            self.progress = True

            def check(reaction, user):
                return user != msg.author

            try:
                while True:
                    reaction_add, user_add = await self.bot.wait_for("reaction_add", timeout = 5 * 60, check = check)
                    if (reaction_add.emoji == "✅"):
                        if (not str(user_add) in self.lobby):
                            self.lobby.append(str(user_add))
                            await ctx.send("{} has joined the lobby.".format(user_add.name))
                        else:
                            await ctx.send("{} is already in the lobby!".format(user_add.name))
                    elif (not self.progress):
                        break

            except asyncio.TimeoutError:
                await self.stopLobby(ctx)

    async def printLobby(self, ctx: commands.Context):
        if (not self.progress):
            await ctx.send("No lobby in progress.")
        elif (len(self.lobby) == 0):
            await ctx.send("Lobby is empty.")
        else:
            msg = ""
            for player in self.lobby:
                msg+= player + "\n"
            await ctx.send(msg)

    async def randomTeams(self, ctx: commands.Context):
        if (not self.author == str(ctx.message.author)):
            await ctx.send("{}, you are not the host of the lobby".format(ctx.message.author.name))
        elif (len(self.lobby) == 0):
            await ctx.send("Lobby is empty.")
        elif (self.progress):
            random.shuffle(self.lobby)

            msg = "Team 1:\n"
            for player in self.lobby[:len(self.lobby)//2]:
                msg += player + "\n"
            
            msg += "\nTeam 2:\n"
            for player in self.lobby[len(self.lobby)//2:]:
                msg += player + "\n"
            
            await ctx.send(msg)
        else:
            await ctx.send("No lobby in progress.")
        
    async def stopLobby(self, ctx: commands.Context):
        if (self.progress and self.author == str(ctx.message.author)):
            self.progress = False
            self.author = ""
            self.lobby.clear()
            self.task.cancel()
            await ctx.send("Lobby is now closed. Please type \".host\" to start a new lobby.")
        else:
            await ctx.send("{}, you are not the host of the lobby".format(ctx.message.author.name))