import discord
from discord.ext import commands
import json

import os


from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all() # or .all() if you ticked all, that is easier
intents.members = True

client = commands.Bot(command_prefix=".",intents=intents)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed=discord.Embed(title=f'{member} has been kicked', color=15158332)
    embed.add_field(name="Reason",value=reason)
    await ctx.send(embed=embed)

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed=discord.Embed(title=f'{member} has been banned', color=15158332)
    embed.add_field(name="Reason",value=reason)
    await ctx.send(embed=embed)

@client.command()
async def addbanword(ctx, word):
    jsonstore = open("bannedwords.json")
    f = json.load(jsonstore)
    print(f)
    foundguild = False
    for item in f:
        print(item)
        if item.get("guildID") == ctx.guild.id:
            print("found")
            foundguild == True 
            item.get("words").append(word)
            with open('bannedwords.json','w') as out_file:
                json.dump(f,out_file,indent=4)
                embed=discord.Embed(title=f'{word} has been banned', color=3066993)
                await ctx.send(embed=embed)
            return


@client.command()
async def setup(ctx):
    jsonstore = open("bannedwords.json")
    f = json.load(jsonstore)
    print(f)
    foundguild = False
    for item in f:
        if hasattr(item, "guildID"):
            if item.get("guildID") == ctx.guild.id:
                print("found")
                foundguild == True 
                return

    if foundguild == False:
        try:
            with open('bannedwords.json','w') as out_file:
                f.append({"guildID":ctx.guild.id,"words":[]})
                json.dump(f,out_file,indent=4)
                embed=discord.Embed(title='Bot has been setup!', color=3066993)
                await ctx.send(embed=embed)
                return
        except:
            embed = discord.Embed(title="Error",color=15158332)
            embed.add_field(name="An Error Occurred")
            await ctx.send(ctx.message.author.mention,embed=embed)
            await ctx.message.delete()
            return



@client.event
async def on_message(message):
    ctx = await client.get_context(message)
    if message.content == "testing":
        await message.channel.send("hello")
    else:
        await client.process_commands(message)

    jsonstore = open("bannedwords.json")
    f = json.load(jsonstore)
    foundguild = False
    for item in f:
        if item.get("guildID") == ctx.guild.id:
            for word in item.get("words"):
                print(word)
                print(ctx.message.content)
                if ctx.message.content.find(word) != -1:
                    await ctx.message.delete()
                    await ctx.send(f"Warning {ctx.message.author.mention}! You are not allowed to say that word in this server")
            return

# run bot      
client.run(TOKEN)

