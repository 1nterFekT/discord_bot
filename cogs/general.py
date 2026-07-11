import disnake
from disnake.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="hello",
        description="Поздороваться с ботом"
    )
    async def hello(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(
            f"Привет, {inter.author.mention}!" 
        )

def setup(bot):
    bot.add_cog(General(bot))