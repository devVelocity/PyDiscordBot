import discord
from discord.ext import commands
import os


from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all() # or .all() if you ticked all, that is easier
intents.members = True

client = commands.Bot(command_prefix=".",intents=intents)

@client.event
async def on_message(message):
    if message.content == "testing":
        await message.channel.send("hello")
    await client.process_commands(message)

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked. Reason={reason}')

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned. Reason={reason}')

# run bot      
client.run(TOKEN)
