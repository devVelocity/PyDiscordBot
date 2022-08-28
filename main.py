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
    embed.add_field(name="Command ran by:",value=ctx.message.author)
    await ctx.send(embed=embed)

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed=discord.Embed(title=f'{member} has been banned', color=15158332)
    embed.add_field(name="Reason",value=reason)
    embed.add_field(name="Command ran by:",value=ctx.message.author)
    await ctx.send(embed=embed)

@client.command()
async def addbanword(ctx, word):
    jsonstore = open("guilddata.json")
    f = json.load(jsonstore)
    print(f)
    foundguild = False
    for item in f:
        print(item)
        if item.get("guildID") == ctx.guild.id:
            print("found")
            foundguild == True 
            item.get("words").append(word)
            with open('guilddata.json','w') as out_file:
                json.dump(f,out_file,indent=4)
                embed=discord.Embed(title=f'"{word}" has been banned', color=3066993)
                # embed.add_field(name="Command ran by:",value=ctx.message.author)
                await ctx.send(ctx.message.author.mention,embed=embed)
            return
    
    ctx.message.delete()

@client.command()
async def removebanword(ctx, word):
    jsonstore = open("guilddata.json")
    f = json.load(jsonstore)
    # print(f)
    foundguild = False
    for item in f:
        # print(item)
        if item.get("guildID") == ctx.guild.id:
            # print("found")
            foundguild == True
            foundword = False
            newarray = []
            for checkword in item.get("words"):
                if checkword != word:
                    newarray.append(checkword)

            item.get("words").pop()
            item["words"] = newarray


            with open('guilddata.json','w') as out_file:
                json.dump(f,out_file,indent=4)
                embed=discord.Embed(title=f'"{word}" has been unbanned', color=3066993)
                # embed.add_field(name="Command ran by:",value=ctx.message.author)
                await ctx.send(ctx.message.author.mention,embed=embed)
            return
    ctx.message.delete()



@client.command()
async def setup(ctx):
    jsonstore = open("guilddata.json")
    f = json.load(jsonstore)
    # print(f)
    foundguild = False
    for item in f:
        if item.get("guildID") == ctx.guild.id:
            foundguild == True 
            embed=discord.Embed(title='Bot has already been previously setup!', color=3066993)
            embed.add_field(name="Tip!",value="Run 'setLogsChannel' with a channel ID to set a channel for message logs")
            await ctx.send(ctx.message.author.mention,embed=embed)
            return

    if foundguild == False:
        try:
            with open('guilddata.json','w') as out_file:
                f.append({"guildID":ctx.guild.id,"words":[],"mods":[],"logsChannel":0})
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

    jsonstore = open("guilddata.json")
    f = json.load(jsonstore)
    foundguild = False
    for item in f:
        if item.get("guildID") == ctx.guild.id:
            for word in item.get("words"):
                # print(word)
                # print(ctx.message.content)
                if ctx.message.content.find(word) != -1:
                    # print(ctx.message.content)
                    if ctx.message.content.find("removebanword") != 1 and ctx.message.content.find("addbanword") != 1:
                        embed = discord.Embed(title="Warning!",description="You are not allowed to say that word in this server",color=15158332)
                        await ctx.send(ctx.message.author.mention,embed=embed)
                        await ctx.message.delete()
                    else:
                        return

            return
    await client.process_commands(message)
# run bot      
client.run(TOKEN)

