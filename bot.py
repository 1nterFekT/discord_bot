import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from utils.logger import setup_logger

load_dotenv()

TOKEN = os.getenv("TOKEN")

logger = setup_logger()

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.InteractionBot(intents=intents)

def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f"cogs.{filename[:-3]}")
            logger.info(f"Загружен cog: {filename}")

@bot.event
async def on_ready():
    logger.info(f"Бот запущен как {bot.user}") # можно использовать .info, .warning, .error

load_cogs()

bot.run(TOKEN)