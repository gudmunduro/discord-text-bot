import os
import commands
import events
import dotenv
from bot import bot

dotenv.load_dotenv()
token = os.getenv("BOT_TOKEN")

bot.run(token)
