from discord.utils import get
import discord
from . import discord_bot
import shelve
from requests_html import HTMLSession   
from bs4 import BeautifulSoup as bs
import urllib.request
import re
import youtube_dl
import asyncio


yt_dl_opts = {'format':'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
ffmpeg_options = {'options':'-vn'}



async def song_request(ctx, command):
  db = shelve.open(discord_bot.dsc_vr)
  video_url = ""
  if len(command) > 1 or not command[1].startswith("https://"):
    search_terms = []

    for x in command[1:]:
      search_terms.append(x)

    url_prefix = 'https://www.youtube.com/results?search_query='

    for x in search_terms:
      url_prefix += "+"+x

    html = urllib.request.urlopen(url_prefix)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    video_url = 'https://www.youtube.com/watch?v=' + video_ids[0]
  else:
    video_url = command[1]
  
  session = HTMLSession()  
  response = session.get(video_url)  
  soup = bs(response.html.html, "html.parser")   
  title = soup.find("meta", itemprop="name")["content"]
  title=re.sub("\(.*?\)","",title)

  music_queue = db['music_queue']
  song_titles = db['song_titles']
  
  
  music_queue.append(video_url)
  song_titles.append(title)
  db['music_queue'] = music_queue
  db['song_titles'] = song_titles
  await ctx.channel.send(f"{title} added to queue")

async def join_voice(ctx, name="Music"):
  voice_channel = discord.utils.get(ctx.guild.voice_channels, name=name)
  voice = discord.utils.get(discord_bot.client.voice_clients, guild=ctx.guild)
  if voice == None:
    await voice_channel.connect()
  else:
    await ctx.channel.send("I'm already in a voice channel!")

async def leave_voice(ctx):
  voice = get(discord_bot.client.voice_clients, guild=ctx.guild)
  if voice == None:
    await ctx.channel.send("I'm not in a voice channel")
  else:
    await voice.disconnect()

async def play(ctx):
  db = shelve.open(discord_bot.dsc_vr)
  url = db['music_queue'][0]
  db.close()
  voice = get(discord_bot.client.voice_clients, guild=ctx.guild)
  if voice == None:
    await ctx.channel.send("I'm not in a voice channel. Send !joinvc *optional voice channel name")
  elif voice.is_playing():
    await ctx.channel.send("I'm already playing in a voice channel")
  else:
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

    song = data['url']
    player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable=discord_bot.ffmpeg_file)
    #voice.play(discord.FFmpegPCMAudio(source=filename),after = lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), discord_class.client.loop))

    voice.play(player,after = lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), discord_class.client.loop))

async def pause(ctx):
  voice = get(discord_bot.client.voice_clients, guild=ctx.guild)
  if voice == None:
    await ctx.channel.send("I'm not in a voice channel")
  else:
    if voice.is_playing():
      await voice.pause()
    else:
      await ctx.channel.send("I'm not currently playing anything")

async def resume(ctx):
  voice = get(discord_bot.client.voice_clients, guild=ctx.guild)
  if voice == None:
    await ctx.channel.send("I'm not in a voice channel")
  else:
    if voice.is_playing():
      await ctx.channel.send("I'm already playing music")
    else:
      await voice.resume()

async def next_song(ctx):
  db = shelve.open(discord_bot.dsc_vr)
  if len(db['music_queue']) <= 1:
    await ctx.channel.send("There are no other songs in the queue")
  else:
    voice = get(discord_bot.client.voice_clients, guild=ctx.guild)
    if voice == None:
      await ctx.channel.send("It looks like I'm not in a voice channel. Use !joinvc *vc name* to add me to one")
    else:
      voice.stop()

async def remove_queue(ctx, queue_num):
  try:
    num = int(queue_num) - 1
  except:
    await ctx.channel.send("Please do !queue *number")

  if num <= len(db['music_queue']):
    db['music_queue'].pop(num)
    await ctx.channel.send(f"{db['song_titles'][num]} has been removed from the queue.")
    db['song_titles'].pop(num)
  else:
    await ctx.channel.send("Please pick a number that's within the queue")
  db.close()

async def previous(ctx):
  db = shelve.open(discord_bot.dsc_vr)
  loop_status = db['loop_status']
  voice = get(discord_bot.client.voice_clients, guild=ctx.guild)
  if loop_status == True:
    queue_to_front = db['music_queue'][len(db['music_queue'])-1]
    title_to_front = db['song_titles'][len(db['song_titles'])-1]
    db['music_queue'].pop(len(db['music_queue'])-1)
    db['song_titles'].pop(len(db['song_titles'])-1)
    db['music_queue'].insert(1,queue_to_front)
    db['song_titles'].insert(1,title_to_front)
    voice.stop()
  else:
    queue_to_front = db['previous_songs'][0]
    db['previous_songs'].pop(0)
    title_to_front = db['previous_titles'][0]
    db['previous_titles'].pop(0)
    db['music_queue'].insert(1,queue_to_front)
    db['song_titles'].insert(1,title_to_front)
    voice.stop()
  db.close()





