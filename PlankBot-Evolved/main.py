import discord
from discord.ext import commands
from scripts.settings import Settings
from data.database import db
from os import listdir

# Database building
db.build()

# Bot initialization
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!pb ", "!plankbot "), intents=intents)

# TODO: CREATE OWN BOT CLASS TO MAKE BETTER READIBILITY

@bot.event
async def on_ready():
    print("Bot ready")


for filename in listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')



# TODO: CREATE OWN BOT CLASS TO MAKE BETTER READIBILITY
bot.run(Settings.token())