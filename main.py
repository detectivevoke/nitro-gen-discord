from discord.ext.commands import BucketType
from discord.ext.commands import cooldown
from webserver import keep_alive
from discord.ext import commands
from discord import Member
from discord import Embed
import webserver
import discord
import random
import string
import os


token=""
prefix = ""
nitro_timeout = 0
welcome = 892126089235816509
bots_channel = 958821741520637992
drop_amount = 1000
whitelist = []




bot = commands.Bot(command_prefix= prefix)
bot.remove_command('help')

#bot events
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"{prefix}help"))
    print(f'Servers: {len(bot.guilds)}')
    print(f'Prefix -> "{prefix}"')
    print("\n")
    print("\n")
    for guild in bot.guilds:
        print(guild.name)


@bot.event
async def on_command_error(ctx, error: Exception):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(color=0xe67e22, description=f'{error}')
        await ctx.send(embed=embed)

@bot.event
async def on_member_join(member):
   await bot.get_channel(welcome).send(f"{member.name} has joined")

@bot.event
async def on_member_remove(member):
   await bot.get_channel(welcome).send(f"{member.name} has left")

#bot commands
@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    staff = discord.utils.get(ctx.guild.roles, name='Owners')
    if staff in ctx.author.roles:
      await member.kick(reason=reason)
      embed = discord.Embed(color=0xe67e22, description=f"{member} has been kicked for {reason}")
      embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/852980461264699443/853177249070055424/logo_1.jpg')
      ctx.send(embed=embed)
@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    staff = discord.utils.get(ctx.guild.roles, name='Owners')
    if staff in ctx.author.roles:
      await member.ban(reason=reason)
      embed = discord.Embed(color=0xe67e22, description=f"{member} has been banned for {reason}")
      embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/852980461264699443/853177249070055424/logo_1.jpg')
      ctx.send(embed=embed)

@bot.command()
async def clear(ctx):
    print(f'{ctx.author} | {ctx.author.id} -> {bot.command_prefix}clear')
    staff = discord.utils.get(ctx.guild.roles, name='Owners')
    if ctx.channel.type != discord.ChannelType.private:
        if staff in ctx.author.roles:
            await ctx.channel.purge(limit=None)
            await ctx.send('https://media.giphy.com/media/3o6Ztm5TtARp8GqssU/giphy.gif')
        else:
            await ctx.message.delete()

@bot.command()
@cooldown(1, nitro_timeout, BucketType.user)
async def nitro(ctx):
  if ctx.channel.id == bots_channel:
        x = 50
        bronze = discord.utils.get(ctx.guild.roles, name='Bronze')#100
        silver = discord.utils.get(ctx.guild.roles, name='Silver')#200
        gold = discord.utils.get(ctx.guild.roles, name='Gold')#300
        premium = discord.utils.get(ctx.guild.roles, name='Premium')#500
        if bronze in ctx.author.roles:
            x += 50
            pass
        else:
            if silver in ctx.author.roles:
                x += 150
                pass
            else:
                if gold in ctx.author.roles:
                    x += 250
                    pass
                else:
                    if premium in ctx.author.roles:
                        x += 450
                        pass
        embed = discord.Embed(color=0xe67e22, description=f'I have sent you {x} nitro codes!')
        await ctx.send(embed = embed)
        while not (x == 0) :
            
            tokens = (''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(16)))
            x -= 1
            a_file = open("nitro.txt", "a" )
            a_file.write('discord.gift/'+tokens + '\n')
            a_file.close()
        target = await bot.fetch_user(ctx.author.id)
        await target.send(file = discord.File(r'nitro.txt'))
        os.remove("nitro.txt")
        print(f'{ctx.author} | {ctx.author.id} -> {prefix}nitro')
        await target.send("All nitro codes are **UNCHECKED**")
        pass
#whitelist
@nitro.after_invoke
async def reset_cooldown(ctx):
    for e in whitelist:
        #to whitelist a person:
        if e == ctx.author.id:
            nitro.reset_cooldown(ctx)
            
        #to whitelist a channel:
        if e == ctx.message.channel.id:
            nitro.reset_cooldown(ctx)
            
        #to whitelist a guild/server:
        if e == ctx.message.guild.id:
            nitro.reset_cooldown(ctx)
            
        #to whitelist a role:
        if e in [role.id for role in ctx.author.roles]:
            nitro.reset_cooldown(ctx)

@bot.command()
async def help(ctx):
    embed = discord.Embed(color=0xe67e22)
    embed.add_field(name='Help', value=f'`{prefix}help`', inline=True)
    embed.add_field(name='Nitro', value=f'`{prefix}nitro`', inline=True)
    embed.add_field(name='Ban', value=f'`{prefix}ban`', inline=True)
    embed.add_field(name='Kick', value=f'`{prefix}kick`', inline=True)
    embed.add_field(name='Clear', value=f'`{prefix}clear`', inline=True)
    embed.add_field(name='Ticket', value=f'`{prefix}ticket`', inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await bot.fetch_user(user_id)
            await target.send(args)

            await ctx.channel.send("'" + args + "' sent to: " + target.name)

        except:
            await ctx.channel.send("Couldn't dm the given user.")
        

    else:
        await ctx.channel.send("You didn't provide a user's id and/or a message.")

@bot.command()
async def drop(ctx):
  staff = discord.utils.get(ctx.guild.roles, name='Owner')
  if staff in ctx.author.roles:
    x = drop_amount
    while not (x == 0) :
      tokens = (''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(16)))
      x -= 1
      a_file = open("drop.txt", "a" )
      a_file.write('discord.gift/'+tokens + '\n')
      a_file.close()
    await ctx.send(file= discord.File(r'drop.txt'))
    os.remove(r'drop.txt')


@bot.command()
async def ticket(ctx):
    print(f'{ctx.author} | {ctx.author.id} -> {bot.command_prefix}ticket')
    if ctx.channel.type != discord.ChannelType.private:
        channels = [str(channel) for channel in bot.get_all_channels()]
        if f'ticket-{ctx.author.id}' in channels:
            await ctx.message.delete()
        else:
            ticket_channel = await ctx.guild.create_text_channel(f'ticket-{ctx.author.id}')
            await ticket_channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
            await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            embed = discord.Embed(color=16083729, description=f'Please enter the reason for this ticket, type `{bot.command_prefix}close` if you want to close this ticket.')
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/852980461264699443/853177249070055424/logo_1.jpg')
            await ticket_channel.send(f'{ctx.author.mention}', embed=embed)
            await ctx.message.delete()



bot.run(token)