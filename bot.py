# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
client = discord.Client()

channels = {}

@client.event
async def on_ready():
  for guild in client.guilds:
    vChannels = guild.voice_channels
    for channel in vChannels:
      channels[channel] = None
  print("ready")
      
async def join(member, chan):
  if chan == None:
    return
  if channels[chan] == None:
    overwrites = {
            chan.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            chan.guild.me: discord.PermissionOverwrite(read_messages=True, manage_permissions=True, manage_channels=True)
            }
    channels[chan] = await chan.guild.create_text_channel(
            "tmp-" +chan.name, category=chan.category, overwrites = overwrites)
  await channels[chan].set_permissions(member, read_messages=True)

async def leave(member, chan):
  if chan==None:
    return
  if channels[chan] == None:
    return
  if len(chan.members) == 0:
    await channels[chan].delete()
    channels[chan] = None
    return
  await channels[chan].set_permissions(member, read_messages=False)

@client.event
async def on_voice_state_update(member, before, after):
    await leave(member, before.channel)
    await join(member, after.channel)

client.run(TOKEN)

