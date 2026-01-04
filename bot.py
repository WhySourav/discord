import discord
from discord.ext import tasks,commands
from dotenv import load_dotenv
from mcstatus import JavaServer
import os

load_dotenv()
intents = discord.Intents.all()
intents.message_content = True
intents.members= True


MC_IP = os.getenv("MC_IP")
MC_PORT = int(os.getenv("MC_PORT"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
server_was_online = False
last_players = set()


bot = commands.Bot(command_prefix='!', intents=intents)
guildid=1455864453462622281


@bot.event
async def on_ready():
    guild = discord.Object(id=guildid)
    await bot.tree.sync(guild=guild)
    print(f"we are in server as {bot.user.name}")
    check_status.start()

@bot.event
async def on_member_join(member):
     channel = bot.get_channel(1455864454242897952)
     await channel.send(f"welcome to the server {member.mention} hii !!")


@bot.event 
async def on_member_remove(member):
     channel = bot.get_channel(1455864454242897952)
     await channel.send(f"{member.mention} left !! hope you enjoyed your stay")


@tasks.loop(seconds=34)
async def check_status():
    global server_was_online, last_players

    channel = bot.get_channel(CHANNEL_ID)
    try:
        server = JavaServer(MC_IP, MC_PORT)
        status = server.status()
        player_names = {p.name for p in status.players.sample} if status.players.sample else set()

        # Server just came online
        if not server_was_online:
            server_was_online = True
            last_players = player_names
            await channel.send(f"@everyone 🟢 \n **Server is ONLINE!** Players: {len(player_names)}/{status.players.max} \n **Join NOW** \n IP - {MC_IP} \n PORT - {MC_PORT}")

        # Check for joins
        joined = player_names - last_players
        left = last_players - player_names

        for p in joined:
            await channel.send(f"➡️ **{p} joined the server!**")

        for p in left:
            await channel.send(f"⬅️ **{p} left the server.**")

        last_players = player_names

    except Exception:
        # Server just went offline
        if server_was_online:
            server_was_online = False
            last_players = set()
            await channel.send(f"@everyone 🔴 **Server is OFFLINE.** \n Hope You enjoyed Your Playtime")



@check_status.before_loop
async def before_check_status():
    await bot.wait_until_ready()
    print("Check loop ready, starting server checks")
    print("--everything looks good to go !!!!!!--")



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
