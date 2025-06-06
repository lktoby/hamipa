import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

activity = discord.Activity(type=discord.ActivityType.playing, name='トビーのパンダ')

bot = commands.Bot(command_prefix='.', intents=intents, activity=activity)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
tree = bot.tree

load_dotenv()
TOKEN = os.getenv('TOKEN')

async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded Cog: {filename[:-3]}")
    await tree.sync()

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

@bot.listen('on_message')
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        await message.channel.send('ん～？')

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)