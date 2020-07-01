import discord
import asyncio
from discord.ext import commands
from our_house_bot.our_house_bot import OurHouse

lobby = set()

class QueueCog(commands.Cog, name = "queue"):
    def __init__(self, bot: OurHouse):
        super().__init__()
        
        self.bot = bot

    @commands.command()
    async def host(self, ctx: commands.Context):
        await self.preparePlayers(ctx)

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
        await ctx.send("Random Mode")

    @commands.command()
    async def lobby(self, ctx: commands.Context):
        await self.printLobby(ctx)

    @commands.command()
    async def stop(self, ctx: commands.Context):
        lobby.clear()
        await ctx.send("Lobby has been cleared.")

    @commands.command()
    async def leave(self, ctx: commands.Context):
        lobby.remove(ctx.message.author)
        await ctx.send("{} has left the lobby.".format(ctx.message.author.name))

    async def preparePlayers(self, ctx: commands.Context):
        msg = await ctx.send("All participants click the ✅ to join. Type \".leave\" to leave.")
        await msg.add_reaction("✅")

        def check(reaction, user):
            return user != msg.author

        try:
            while True:
                reaction_add, user_add = await self.bot.wait_for("reaction_add", timeout = 60.0, check = check)
                if (reaction_add.emoji == "✅"):
                    lobby.add(user_add)
                    await ctx.send("{} has joined the lobby.".format(user_add.name))

        except asyncio.TimeoutError:
            await ctx.send("Lobby time over. Pick game mode.")

    async def printLobby(self, ctx: commands.Context):
        if (len(lobby) == 0):
            await ctx.send("Lobby is empty.")
        else:
            msg = ""
            for player in lobby:
                msg+= str(player) + "\n"
            await ctx.send(msg)