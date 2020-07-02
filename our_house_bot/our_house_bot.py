from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand

class OurHouse(commands.Bot):
    def __init__(self, **options):
        super().__init__(".", help_command = None, **options)

        self.discord_token = discord_token

        from our_house_bot.cogs.queue_cog import QueueCog
        self.add_cog(QueueCog(self))

    def run(self, *args, **kwargs):
        super().run(self.discord_token, *args, **kwargs)

    async def on_ready(self):
        print("Bot is ready!")