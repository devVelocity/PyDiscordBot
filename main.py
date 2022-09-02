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
# client.remove_command('help')

# TODO - add todo shit here


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
        embed = discord.Embed(title=f"Moderation Controls for User: {member}",color=16776960)
        if reason:
            embed.add_field(name="Reason for Moderation:",value=reason)

        embed.add_field(name="⠀",value="Type 'cancel' to cancel the action.",inline=False)

        button1 = Button(label="Kick",style=discord.ButtonStyle.red)
        button2 = Button(label="Ban",style=discord.ButtonStyle.red)
        button3 = Button(label="Timeout",style=discord.ButtonStyle.blurple)
        cancelButton = Button(label="Cancel",style=discord.ButtonStyle.gray)
        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        originalmsg = await ctx.send(embed=embed,view=view)


        async def kick_callback(interaction):
            try:
                button1.style=discord.ButtonStyle.gray
                button2.style=discord.ButtonStyle.gray
                button3.style=discord.ButtonStyle.gray
                if interaction.user.id == ctx.message.author.id:
                    if ctx.message.author.id == member.id:
                        embed = discord.Embed(title="You cannot kick yourself.",color=15158332)
                        await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)
                        await ctx.message.delete()
                        await originalmsg.delete()
                    else:
                        await member.kick(reason=reason)
                        kickembed=discord.Embed(title=f'{member} has been kicked', color=16776960)
                        kickembed.add_field(name="Reason",value=reason)
                        kickembed.add_field(name="Command ran by:",value=ctx.message.author)
                        await sendLog({"guildid":ctx.guild.id,"logtitle":f"{member} has been kicked","ranby":ctx.message.author.id,"reason":reason})  
                        await ctx.send(ctx.message.author.mention,embed=kickembed)
                        await ctx.message.delete()
                        await originalmsg.delete()
                else:
                    await interaction.response.send_message("Sorry, you do not have access to this button",ephemeral=True)
            except:
                await originalmsg.delete()

        async def ban_callback(interaction):
            try:
                button1.style=discord.ButtonStyle.gray
                button2.style=discord.ButtonStyle.gray
                button3.style=discord.ButtonStyle.gray
                if interaction.user.id == ctx.message.author.id:
                    if ctx.message.author.id == member.id:
                        embed = discord.Embed(title="You cannot ban yourself.",color=15158332)
                        await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)
                        await ctx.message.delete()
                        await originalmsg.delete()

                    else:
                        await member.ban(reason=reason)
                        banembed=discord.Embed(title=f'{member} has been banned', color=16776960)
                        banembed.add_field(name="Reason",value=reason)
                        banembed.add_field(name="Command ran by:",value=ctx.message.author)
                        await sendLog({"guildid":ctx.guild.id,"logtitle":f"{member} has been banned","ranby":ctx.message.author.id,"reason":reason})  
                        await ctx.send(ctx.message.author.mention,embed=banembed)
                        await ctx.message.delete()
                        await originalmsg.delete()
                else:
                    await interaction.response.send_message("Sorry, you do not have access to this button",ephemeral=True)
            except:
                await originalmsg.delete()

        async def timeout_callback(interaction):
            
            
            try:
                button1.style=discord.ButtonStyle.gray
                button2.style=discord.ButtonStyle.gray
                button3.style=discord.ButtonStyle.gray
                if interaction.user.id == ctx.message.author.id:

                    
                    timeoutembed = discord.Embed(title=f"Timeout Controls for: {member}",color=16776960)
                    timeoutembed.add_field(name="Reason for Timeout:",value=reason)
                    select = Select(placeholder="Choose a option.",options=[discord.SelectOption(label="1m"),discord.SelectOption(label="10m"),discord.SelectOption(label="1hr"),discord.SelectOption(label="Custom")])
                    newview = View()
                    newview.add_item(select)
                    cancelButton = Button(label="Cancel",style=discord.ButtonStyle.red)
                    newview.add_item(cancelButton)
                    await originalmsg.delete()

                    sendselect = await ctx.send(ctx.message.author.mention,embed=timeoutembed,view=newview)

                    async def cancel_callback(interaction):
                        if interaction.user.id == ctx.message.author.id:
                            await sendselect.delete()
                            embed = discord.Embed(title="Timeout Cancelled",color=15158332)
                            await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)

                    cancelButton.callback = cancel_callback

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
                                await sendLog({"guildid":ctx.guild.id,"logtitle":f"{member} has been timed out for 1 minute","ranby":ctx.message.author.id,"reason":reason,"channel":ctx.message.channel.id}) 

                            elif select.values[0] == '10m':
                                delta = timedelta(
                                    minutes=10
                                )
                                embed.title = f"{member} has been timed out for 10 minutes."
                                await member.timeout(delta, reason=reason)
                                await sendLog({"guildid":ctx.guild.id,"logtitle":f"{member} has been timed out for 10 minutes","ranby":ctx.message.author.id,"reason":reason,"channel":ctx.message.channel.id}) 
                            elif select.values[0] == '1hr':
                                delta = timedelta(
                                    hours=1
                                )
                                embed.title = f"{member} has been timed out for 1 hour."
                                await member.timeout(delta, reason=reason)
                                await sendLog({"guildid":ctx.guild.id,"logtitle":f"{member} has been timed out for 1 hour","ranby":ctx.message.author.id,"reason":reason,"channel":ctx.message.channel.id}) 
                            elif select.values[0] == '1d':
                                delta = timedelta(
                                    days=1
                                )
                                embed.title = f"{member} has been timed out for 1 day."
                                await member.timeout(delta, reason=reason)
                                await sendLog({"guildid":ctx.guild.id,"logtitle":f"{member} has been timed out for 1 day","ranby":ctx.message.author.id,"reason":reason,"channel":ctx.message.channel.id})
                            elif select.values[0] == 'Custom':
                                await sendselect.delete()
                                embed = discord.Embed(title="Input the amount of time (minutes,hours,days). Up until a maximum of 28 days",color=16776960)
                            
                                timeSpecify = await ctx.message.channel.send(embed=embed)
                                def check(m):
                                    return m.content and m.channel == ctx.message.channel and m.author == ctx.message.author
                                msg = await client.wait_for('message',check=check)
                                msgsplit = msg.content.split(",")
                                minutes = 0
                                hours = 0
                                days = 0
                                if msgsplit[0]:
                                    minutes = int(msgsplit[0])
                                if msgsplit[1]:
                                    hours = int(msgsplit[1])
                                if msgsplit[2]:
                                    days = int(msgsplit[2])

                                delta = timedelta(
                                    minutes=minutes,
                                    hours=hours,
                                    days=days
                                )
                                await timeSpecify.delete()
                                embed = discord.Embed(title=f"{member} has been timed out for {msgsplit[0]}m, {msgsplit[1]}h and {msgsplit[2]}d",color=3066993)
                                embed.add_field(name="Reason",value=reason)
                                await msg.delete()
                                await ctx.send(ctx.message.author.mention, embed=embed,delete_after=30)
                                await member.timeout(delta, reason=reason)
                                await sendLog({"guildid":ctx.guild.id,"logtitle":f"{member} has been timed out for {msgsplit[0]}m, {msgsplit[1]}h and {msgsplit[2]}d","ranby":ctx.message.author.id,"reason":reason,"channel":ctx.message.channel.id})
                        except:
                            await sendselect.delete()


                        await sendselect.delete()
                        await ctx.send(ctx.message.author.mention,embed=embed,delete_after=30)
                        await ctx.message.delete()
                else:
                    await interaction.response.send_message("Sorry, you do not have access to this button",ephemeral=True)

                select.callback = select_callback
            except:
                await sendselect.delete()



        button1.callback = kick_callback
        button2.callback = ban_callback
        button3.callback = timeout_callback
        
        def check(m):
            return m.content and m.channel == ctx.message.channel and m.author == ctx.message.author
        
        msg = await client.wait_for('message',check=check)
        if msg.content.lower() == "cancel":
            await msg.delete()
            button1.style=discord.ButtonStyle.gray
            button2.style=discord.ButtonStyle.gray
            button3.style=discord.ButtonStyle.gray
            embed = discord.Embed(title="Moderation Cancelled",color=15158332 	)
            await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)
            await originalmsg.delete()
            await ctx.message.delete()
    

@client.command()
async def purge(ctx,*,amt):
    if moderatorcheck(ctx.message.author.id) == True:
        if int(amt) > 10:
            embed = discord.Embed(title="You cannot purge over 10 messages at a time.",color=15158332)
            await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)
        else:
            embed = discord.Embed(title=f"{amt} messages have been purged.",color=3066993)
            await ctx.channel.purge(limit=int(amt) + 1)
            await ctx.send(ctx.message.author.mention,embed=embed,delete_after=20)
            await sendLog({"guildid":ctx.guild.id,"logtitle":f"{amt} messages has been purged.","ranby":ctx.message.author.id,"channel":ctx.message.channel.id})
    await ctx.message.delete()



@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if moderatorcheck(ctx.message.author.id) == True:
        if ctx.message.author.id == member.id:
            embed = discord.Embed(title="You cannot kick yourself.",color=15158332)
            await ctx.send(embed=embed)
        else:
            await member.kick(reason=reason)
            embed=discord.Embed(title=f'{member} has been kicked', color=15158332)
            embed.add_field(name="Reason",value=reason)
            embed.add_field(name="Command ran by:",value=ctx.message.author)
            await sendLog({"guildid":ctx.guild.id,"logtitle":f"{member} has been kicked","ranby":ctx.message.author.id,"reason":reason,"channel":ctx.message.channel.id})  
            await ctx.send(embed=embed)

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if moderatorcheck(ctx.message.author.id) == True:
        if ctx.message.author.id == member.id:
            embed = discord.Embed(title="You cannot ban yourself.",color=15158332)
            await ctx.send(embed=embed)
        else:
            await member.ban(reason=reason)
            embed=discord.Embed(title=f'{member} has been banned', color=15158332)
            embed.add_field(name="Reason",value=reason)
            embed.add_field(name="Command ran by:",value=ctx.message.author)
            await sendLog({"guildid":ctx.guild.id,"logtitle":f"{member} has been banned","ranby":ctx.message.author.id,"reason":reason,"channel":ctx.message.channel.id})   
            await ctx.send(embed=embed)


async def sendLog(data):
    print(data)
    jsonstore = open("guilddata.json")
    f = json.load(jsonstore)
    for item in f:
        if item.get("guildID") == data.get("guildid"):
            await client.wait_until_ready()
            channel = client.get_channel(item.get("logsChannel"))
            embed = discord.Embed(title=data.get("logtitle"),color=16776960)
            getuser = client.get_user(data.get("ranby"))
            embed.add_field(name="Command ran by:",value=getuser.mention)
            getchannel = client.get_channel(data.get("channel"))
            embed.add_field(name="Sent in:",value=getchannel.mention)
            if data.get("reason"):
                embed.add_field(name="Reason",value=data["reason"],inline=False)
            await channel.send(embed=embed)



@client.command()
async def setlog(ctx,*,channel):
    if moderatorcheck(ctx.message.author.id) == True:
        jsonstore = open("guilddata.json")
        f = json.load(jsonstore)
        print("channel")
        if channel == "-rm":
            for item in f:
                if item.get("guildID") == ctx.guild.id:
                    with open('guilddata.json','w') as out_file:
                        item["logsChannel"] = int(0)
                        print("log change")
                        json.dump(f,out_file,indent=4)

                    embed=discord.Embed(title=f'Logs Channel has been removed!', color=15158332)
                    # embed.add_field(name="Command ran by:",value=ctx.message.author)
                    await ctx.message.delete()
                    await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)
        else:
            for item in f:
                if item.get("guildID") == ctx.guild.id:
                    with open('guilddata.json','w') as out_file:
                        item["logsChannel"] = int(channel)
                        print("log change")
                        json.dump(f,out_file,indent=4)

                    embed=discord.Embed(title=f'Logs Channel has been set!', color=3066993)
                    # embed.add_field(name="Command ran by:",value=ctx.message.author)
                    await ctx.message.delete()
                    await sendLog({"guildid":ctx.guild.id,"logtitle":f"Logs channel has been set to {channel}","ranby":ctx.message.author.id,"channel":ctx.message.channel.id})
                    await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)



@client.command()
async def addbanword(ctx, word):
    if moderatorcheck(ctx.message.author.id) == True:
        jsonstore = open("guilddata.json")
        f = json.load(jsonstore)
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
                
                await sendLog({"guildid":ctx.guild.id,"logtitle":f"{word} has been added to the word banlist","ranby":ctx.message.author.id,"channel":ctx.message.channel.id})                    
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
                
                await sendLog({"guildid":ctx.guild.id,"logtitle":f"{word} has been removed from the word banlist","ranby":ctx.message.author.id,"channel":ctx.message.channel.id})                     
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
                embed.add_field(name="Additional Tip:",value="Run 'setlog' with a Channel ID to set a Channel for Message Logs.")
                embed.add_field(name="Additional Tip:",value="Run 'addmod' mentioning a User to add a Moderator.")
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
                        await ctx.send(ctx.message.author.mention,embed=embed,delete_after=20)
                    
                    await sendLog({"guildid":ctx.guild.id,"logtitle":f"{member} has been added to the Moderator List","ranby":ctx.message.author.id,"channel":ctx.message.channel.id})                    
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
                            embed = discord.Embed(title=f"{member} has been removed from the Moderator List.",color=15158332)
                            await ctx.message.delete()
                            await ctx.send(ctx.message.author.mention,embed=embed,delete_after=20)
                        
                        await sendLog({"guildid":ctx.guild.id,"logtitle":f"{member} has been removed from the Moderator List","ranby":ctx.message.author.id,"channel":ctx.message.channel.id})                    
                        return
                    else:
                        embed = discord.Embed(title=f"You cannot remove the Server Owner from the Moderator List",color=15158332)
                        await ctx.message.delete()
                        await ctx.send(ctx.message.author.mention,embed=embed,delete_after=10)
                else:
                    embed = discord.Embed(title=f"{member} is not on the Moderator List.",color=15158332)
                    await ctx.message.delete()
                    await ctx.send(ctx.message.author.mention,embed=embed)
    # run bot      

def contains_word(text, word):
    return bool(re.search(r'\b' + re.escape(word) + r'\b', text))

#detect deleted message
@client.event
async def on_message_delete(message, member):
    if message.author.id == client.user.id:
        jsonstore = open("guilddata.json")
        f = json.load(jsonstore)
        for item in f:
            if item.get("logsChannel") != 0:
                if item.get("deleteLogs") == True:
                    await sendLog({"guildid":message.guild.id,"logtitle":f"{member} has deleted a message in {message.channel}","channel":message.channel.id})                    

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

