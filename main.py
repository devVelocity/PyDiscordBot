import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from datetime import timedelta
import json
import re

import os


from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all() # or .all() if you ticked all, that is easier
intents.members = True

client = commands.Bot(command_prefix=".",intents=intents)
client.remove_command('help')

def moderatorcheck(modid):
    jsonstore = open("guilddata.json")
    f = json.load(jsonstore)
    for item in f:
        for mods in item.get("mods"):
            if mods == modid:
                return True

@client.command()
async def mod(ctx, member: discord.Member, *, reason=None):
    if moderatorcheck(ctx.message.author.id) == True:
            
        await ctx.message.delete()
        embed = discord.Embed(title=f"Moderator Controls for User: {member}",color=16776960)
        button1 = Button(label="Kick",style=discord.ButtonStyle.blurple)
        button2 = Button(label="Ban",style=discord.ButtonStyle.blurple)
        button3 = Button(label="Timeout",style=discord.ButtonStyle.blurple)
        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        originalmsg = await ctx.send(embed=embed,view=view)

        async def kick_callback(interaction):
            try:
                if interaction.user.id == ctx.message.author.id:
                    await member.kick(reason=reason)
                    kickembed=discord.Embed(title=f'{member} has been kicked', color=16776960)
                    kickembed.add_field(name="Reason",value=reason)
                    kickembed.add_field(name="Command ran by:",value=ctx.message.author)
                    await ctx.send(ctx.message.author.mention,embed=kickembed)
                    await ctx.message.delete()
                    await originalmsg.delete()
                else:
                    await interaction.response.send_message("Sorry, you do not have access to this command",ephemeral=True)
            except:
                await originalmsg.delete()

        async def ban_callback(interaction):
            try:
                if interaction.user.id == ctx.message.author.id:
                    await member.ban(reason=reason)
                    banembed=discord.Embed(title=f'{member} has been banned', color=16776960)
                    banembed.add_field(name="Reason",value=reason)
                    banembed.add_field(name="Command ran by:",value=ctx.message.author)
                    await ctx.send(ctx.message.author.mention,embed=banembed)
                    await ctx.message.delete()
                    await originalmsg.delete()
                else:
                    await interaction.response.send_message("Sorry, you do not have access to this command",ephemeral=True)
            except:
                await originalmsg.delete()

        async def timeout_callback(interaction):
            try:
                if interaction.user.id == ctx.message.author.id:
                    timeoutembed = discord.Embed(title=f"Timeout Controls for: {member}",color=16776960)
                    timedoutmsg = await ctx.send(ctx.message.author.mention,embed=timeoutembed)
                    select = Select(placeholder="Choose a option.",options=[discord.SelectOption(label="1m"),discord.SelectOption(label="5m"),discord.SelectOption(label="10m"),discord.SelectOption(label="1hr"),discord.SelectOption(label="4hr"),discord.SelectOption(label="1d")])
                    newview = View()
                    newview.add_item(select)
                    await originalmsg.delete()
                    sendselect = await ctx.send(view=newview)

                    async def select_callback(interaction):
                        try:
                            print(select.values)
                            embed = discord.Embed(title=f"",color=3066993)
                            embed.add_field(name="Reason",value=reason)
                            if select.values[0] == '1m':
                                delta = timedelta(
                                    seconds=60
                                )
                                embed.title = f"{member} has been timed out for 1 minute."
                                await member.timeout(delta, reason=reason)
                            elif select.values[0] == '5m':
                                delta = timedelta(
                                    minutes=5
                                )
                                embed.title = f"{member} has been timed out for 5 minutes."
                                await member.timeout(delta, reason=reason)
                            elif select.values[0] == '10m':
                                delta = timedelta(
                                    minutes=10
                                )
                                embed.title = f"{member} has been timed out for 10 minutes."
                                await member.timeout(delta, reason=reason)
                            elif select.values[0] == '1hr':
                                delta = timedelta(
                                    hours=1
                                )
                                embed.title = f"{member} has been timed out for 1 hour."
                                await member.timeout(delta, reason=reason)
                            elif select.values[0] == '4hr':
                                delta = timedelta(
                                    hours=4
                                )
                                embed.title = f"{member} has been timed out for 4 hours."
                                await member.timeout(delta, reason=reason)
                            elif select.values[0] == '1d':
                                delta = timedelta(
                                    days=1
                                )
                                embed.title = f"{member} has been timed out for 1 day."
                                await member.timeout(delta, reason=reason)
                        except:
                            await sendselect.delete()
                            await timedoutmsg.delete()
                            await ctx.message.delete()

                        await sendselect.delete()
                        await timedoutmsg.delete()
                
                        await ctx.send(ctx.message.author.mention,embed=embed)
                        await ctx.message.delete()
                else:
                    await interaction.response.send_message("Sorry, you do not have access to this command",ephemeral=True)

                select.callback = select_callback
            except:
                await sendselect.delete()
                await timedoutmsg.delete()



        button1.callback = kick_callback
        button2.callback = ban_callback
        button3.callback = timeout_callback
    


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if moderatorcheck(ctx.message.author.id) == True:
        await member.kick(reason=reason)
        embed=discord.Embed(title=f'{member} has been kicked', color=15158332)
        embed.add_field(name="Reason",value=reason)
        embed.add_field(name="Command ran by:",value=ctx.message.author)
        await ctx.send(embed=embed)

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if moderatorcheck(ctx.message.author.id) == True:
        await member.ban(reason=reason)
        embed=discord.Embed(title=f'{member} has been banned', color=15158332)
        embed.add_field(name="Reason",value=reason)
        embed.add_field(name="Command ran by:",value=ctx.message.author)
        await ctx.send(embed=embed)

@client.command()
async def addbanword(ctx, word):
    if moderatorcheck(ctx.message.author.id) == True:
        jsonstore = open("guilddata.json")
        f = json.load(jsonstore)
        print(f)
        foundguild = False
        for item in f:
            if item.get("guildID") == ctx.guild.id:
                print("found")
                foundguild == True 
                item.get("words").append(word)
                with open('guilddata.json','w') as out_file:
                    json.dump(f,out_file,indent=4)
                    await ctx.message.delete()
                    embed=discord.Embed(title=f'"{word}" has been added to the word banlist.', color=3066993)
                    # embed.add_field(name="Command ran by:",value=ctx.message.author)
                    await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)
                return
        
        ctx.message.delete()

@client.command()
async def removebanword(ctx, word):
    if moderatorcheck(ctx.message.author.id) == True:
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
                    await ctx.message.delete()
                    embed=discord.Embed(title=f'"{word}" has been removed from the word banlist', color=3066993)
                    # embed.add_field(name="Command ran by:",value=ctx.message.author)
                    await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)
                return
        ctx.message.delete()



@client.command()
async def setup(ctx):
    if ctx.message.author.id == ctx.message.guild.owner_id:
        jsonstore = open("guilddata.json")
        f = json.load(jsonstore)
        # print(f)
        foundguild = False
        for item in f:
            if item.get("guildID") == ctx.guild.id:
                foundguild == True 
                embed=discord.Embed(title='Bot has already been previously setup!', color=3066993)
                embed.add_field(name="Additional Tip:",value="Run 'setLogsChannel' with a Channel ID to set a Channel for Message Logs.")
                embed.add_field(name="Additional Tip:",value="Run 'addModerator' with a User ID to add a Moderator.")
                await ctx.send(ctx.message.author.mention,embed=embed)
                return

        if foundguild == False:
            try:
                with open('guilddata.json','w') as out_file:
                    f.append({"guildID":ctx.guild.id,"words":[],"mods":[ctx.message.guild.owner_id],"logsChannel":0})
                    embed=discord.Embed(title='Bot has been setup!', color=3066993)
                    embed.add_field(name="Additional Tip:",value="Run 'setLogsChannel' with a Channel ID to set a Channel for Message Logs.")
                    embed.add_field(name="Additional Tip:",value="Run 'addModerator' with a User ID to add a Moderator.")
                    json.dump(f,out_file,indent=4)
                    await ctx.send(embed=embed,delete_after=10)
                    return
            except Exception as e:
                embed = discord.Embed(title="Error",color=15158332)
                embed.add_field(name="Error:",value=e)
                await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)
                await ctx.message.delete()
                return


@client.command()
async def checkbannedwords(ctx):
    if moderatorcheck(ctx.message.author.id) == True:
        jsonstore = open("guilddata.json")
        f = json.load(jsonstore)
        embed=discord.Embed(title=f'Banned words in Server "{ctx.guild.name}"', color=16776960)
        for item in f:
            if item.get("guildID") == ctx.guild.id:
                if len(item.get("words")) == 0:
                    embed.color = 15158332
                    embed.add_field(name=f"Error",value="There are no banned words in this server")
                else:
                    for word in item.get("words"):
                        embed.add_field(name="⠀",value=f"{word}")
        
        await ctx.message.delete()
        await ctx.send(ctx.message.author.mention, embed=embed)

@client.command()
async def addmod(ctx, member: discord.Member):
    if moderatorcheck(ctx.message.author.id) == True:
        jsonstore = open("guilddata.json")
        f = json.load(jsonstore)
        foundguild = False
        for item in f:
            if item.get("guildID") == ctx.guild.id:
                if member.id in item.get("mods"):
                    embed = discord.Embed(title=f"{member} is already on the Moderator List.",color=15158332)
                    await ctx.message.delete()
                    await ctx.send(ctx.message.author.mention,embed=embed)
                else:
                    with open('guilddata.json','w') as out_file:
                        item.get("mods").append(member.id)
                        json.dump(f,out_file,indent=4)
                        embed = discord.Embed(title=f"{member} has been added to the Moderator List.",color=3066993)
                        await ctx.message.delete()
                        await ctx.send(ctx.message.author.mention,embed=embed)
                    return

@client.command()
async def rmmod(ctx, member: discord.Member):
    if moderatorcheck(ctx.message.author.id) == True:
        jsonstore = open("guilddata.json")
        f = json.load(jsonstore)
        foundguild = False
        for item in f:
            if item.get("guildID") == ctx.guild.id:
                if member.id in item.get("mods"):
                    if member.id != ctx.message.guild.owner_id:
                        with open('guilddata.json','w') as out_file:
                            valuetopop = item.get("mods").index(member.id)
                            item.get("mods").pop(valuetopop)
                            json.dump(f,out_file,indent=4)
                            embed = discord.Embed(title=f"{member} has been removed to the Moderator List.",color=3066993)
                            await ctx.message.delete()
                            await ctx.send(ctx.message.author.mention,embed=embed)
                        return
                    else:
                        embed = discord.Embed(title=f"You cannot remove the Owner from the Moderator List",color=15158332)
                        await ctx.message.delete()
                        await ctx.send(ctx.message.author.mention,embed=embed)
                else:
                    embed = discord.Embed(title=f"{member} is not on the Moderator List.",color=15158332)
                    await ctx.message.delete()
                    await ctx.send(ctx.message.author.mention,embed=embed)
    # run bot      

def contains_word(text, word):
    return bool(re.search(r'\b' + re.escape(word) + r'\b', text))

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
                if ctx.message.content.lower().find(word) != -1:
                    # print("through")
                    if len(ctx.message.content.lower()) == len(word):
                        if word == ctx.message.content.lower():
                            await ctx.message.delete()
                            embed = discord.Embed(title="Warning!",description="You are not allowed to say that word in this server.",color=15158332)
                            await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)
                    else:
                        if contains_word(ctx.message.content, word):
                            # print(ctx.message.content)
                            if ctx.message.content.find("removebanword") != 1 and ctx.message.content.find("addbanword") != 1:
                                await ctx.message.delete()
                                embed = discord.Embed(title="Warning!",description="You are not allowed to say that word in this server.",color=15158332)
                                await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)
                            else:
                                return

            return
    await client.process_commands(message)

client.run(TOKEN)

