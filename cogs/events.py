import disnake
from disnake.ext import commands
from utils.logger import logger


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Бот запущен как {self.bot.user}")


def setup(bot):
    bot.add_cog(Events(bot))
