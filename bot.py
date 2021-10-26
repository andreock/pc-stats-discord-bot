import discord
import cpuinfo
import psutil as p
import os
from discord.ext import commands
from discord.ext.commands import bot
import sys
import shutil
import subprocess
import re


def size(byte):
  #this the function to convert bytes into more suitable reading format.

  #Suffixes for the size
  for x in ["B","KB","MB","GB","TB"]:
    if byte<1024:
      return f"{byte:.2f}{x}"
    byte=byte/1024


fre=p.cpu_freq()
client = commands.Bot(command_prefix='.')
info = cpuinfo.get_cpu_info()['brand_raw']
core = 'I have ' , p.cpu_count(logical=False), 'core'
maxfrequency = "Maximum Frequency:" ,fre.max, "Mhz"
minfreq = "Minimum Frequency:", fre.min,"Mhz"
currentfreq = "Current Frequency: ",fre.current ,"Mhz"
cpusage = "Total CPU Usage:", p.cpu_percent()
mem = p.virtual_memory()
allram = "Total Memory:    ",size(mem.total)
availableram = "Available Memory:", size(mem.available)
usedram = "Used Memory:     ", size(mem.used), "percentual", mem.percent,"%"

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def cpu(ctx):
    await ctx.send(core)
    await ctx.send(maxfrequency)
    await ctx.send(minfreq)
    await ctx.send(currentfreq)
    await ctx.send(cpusage)

@client.command()
async def ram(ctx):
    await ctx.send(allram)
    await ctx.send(availableram)
    await ctx.send(usedram)

@client.command()
async def disk(ctx):
    await ctx.send(allram)
    await ctx.send(availableram)
    await ctx.send(usedram)

@client.command()
async def hw(ctx):
    if cpuinfo.get_cpu_info()['vendor_id_raw'] == 'GenuineIntel':
        result = subprocess.run(["./gpu.sh"], stdout=subprocess.PIPE)
        disk = subprocess.run(["./disk.sh"], stdout=subprocess.PIPE)
        name = subprocess.run(["cat" ,"/proc/sys/kernel/hostname"], stdout=subprocess.PIPE)
        embed=discord.Embed(title=name.stdout, description="Here the specs of the pc")
        embed.set_author(name=name.stdout, icon_url="https://pbs.twimg.com/profile_images/1301470406545637376/ti9zFC98_400x400.png")
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1301470406545637376/ti9zFC98_400x400.png")
        embed.add_field(name="Cpu", value=info, inline=False)
        embed.add_field(name="Ram", value=allram, inline=True)
        embed.add_field(name="Disk", value=disk.stdout, inline=True)
        embed.add_field(name="Gpu", value=result.stdout, inline=True)
        await ctx.send(embed=embed)
    else:
        result = subprocess.run(["./gpu.sh"], stdout=subprocess.PIPE)
        disk = subprocess.run(["./disk.sh"], stdout=subprocess.PIPE)
        name = subprocess.run(["cat" ,"/proc/sys/kernel/hostname"], stdout=subprocess.PIPE)
        embed=discord.Embed(title=name.stdout, description="Here the specs of the pc")
        embed.set_author(name=name.stdout, icon_url="https://www.amd.com/system/files/2020-06/amd-default-social-image-1200x628.jpg")
        embed.set_thumbnail(url="https://www.amd.com/system/files/2020-06/amd-default-social-image-1200x628.jpg")
        embed.add_field(name="Cpu", value=info, inline=False)
        embed.add_field(name="Ram", value=allram, inline=True)
        embed.add_field(name="Disk", value=disk.stdout, inline=True)
        embed.add_field(name="Gpu", value=result.stdout, inline=True)
        await ctx.send(embed=embed)

client.run('TOKEN')
