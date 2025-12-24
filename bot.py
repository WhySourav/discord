import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
intents = discord.Intents.all()
intents.message_content = True
intents.members= True

bot = commands.Bot(command_prefix='!', intents=intents)
guildid=1451929149131198538


     



@bot.event
async def on_ready():
    guild = discord.Object(id=guildid)
    await bot.tree.sync(guild=guild)
    print(f"we are in server as {bot.user.name}")


@bot.event
async def on_member_join(member):
     channel = bot.get_channel(1452005170836934798)
     await channel.send(f"welcome to the server {member.mention}!")


@bot.event 
async def on_member_remove(member):
     channel = bot.get_channel(1452005170836934798)
     await channel.send(f"{member.mention} left !! hope you enjoyed your stay")


@bot.command()
async def hii(ctx):
      await ctx.send("hello there whts up!!")


@bot.tree.command(name = "ping", description="Get the bot's latency", guild=discord.Object(id=guildid))
async def pingme(interaction: discord.Interaction):
      latency = bot.latency * 1000 
      await interaction.response.send_message(f"🏓Pong! `{latency:.2f}`ms")        

@bot.tree.command(name = "say", description="Make the bot sayy something",guild=discord.Object(id=guildid))
async def say(interaction: discord.Interaction, message: str):
      await interaction.response.send_message(message)      



@bot.tree.command(name="userinfo", description="get info about user",guild=discord.Object(id=guildid))
async def userinfo(interaction: discord.Interaction,member: discord.Member):
      await interaction.response.send_message(f" 👤  User Name: {member.name}\n User ID: {member.id}\n User Joined at: {member.joined_at.date()}\n User Created at: {member.created_at}")






bot.run(os.getenv("TOKEN"))
