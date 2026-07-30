import os
import disnake
from disnake.ext import commands

from config import STABLE_TOKEN, BETA_TOKEN
from utils.logger import logger

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.InteractionBot(intents=intents)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")
        logger.info(f"Загружен cog: {filename}")

bot.run(STABLE_TOKEN)
