import discord
from discord.ext import commands
from discord.embeds import Embed
import os


from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all() # or .all() if you ticked all, that is easier
intents.members = True

client = commands.Bot(command_prefix=".",intents=intents)

@client.event
async def on_message(message):
    print("aaaaaaaaaa")
    print(message.content)
    if message.content == "testing":
        print("hi")
        await message.channel.send("hello")
client.run(TOKEN)
