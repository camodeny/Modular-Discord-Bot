'''
Init module

Finished:
-Houses client object inside discord_bot class
-Sets up core functions of the bot
-Verifies dsc_vr file is online and has necessary variables initiated
-Sets command prefix and secret key in long form storage
-Handles command prefix checks

wip:

'''


#cause discord bot obviously
import discord
#this is the variable storage method I'm using. This allows us to save variables to files instead of memory. Slows down performance in some areas but it allows things to stay persistent between runs
import shelve
#os.path allows me to create files in the correct directory. So if I need to make a file it will end up wherever the program is instead of like making it on the desktop
from os.path import dirname, join
from os.path import exists


class discord_bot():
  #creates client object
  client = discord.Client(intents=discord.Intents.all())
  #file location for dsc_vr
  dsc_vr = join(dirname(dirname(__file__)), 'discord_modules', 'dsc_vr')
  #file location for dsc_poll
  dsc_poll = join(dirname(dirname(__file__)), 'discord_modules','dsc_poll')
  #file location for dsc_mod
  dsc_mod = join(dirname(dirname(__file__)), 'discord_modules','dsc_mod')
  #file location for dsc_give
  dsc_give = join(dirname(dirname(__file__)), 'discord_modules', 'dsc_give')
  #file location for ffmpeg
  ffmpeg_file = join(dirname(dirname(__file__)), 'discord_modules','ffmpeg')
  #First function to be run
  def __init_bot__():
    import ctypes
    import ctypes.util
 
    print("ctypes - Find opus:")
    a = ctypes.util.find_library('opus')
    print(a)
 
    print("Discord - Load Opus:")
    b = discord.opus.load_opus(a)
    print(b)
 
    print("Discord - Is loaded:")
    c = discord.opus.is_loaded()
    print(c)
    
    db = shelve.open(discord_bot.dsc_vr)
    if db['secret_key'] == None:
      db['secret_key'] = input("Please input your secret key: ")
    if db['cmd_prefix'] == None:
      db['cmd_prefix'] = input('please input your command prefix: ')
    secret_key = db['secret_key']
    db.close()

    discord_bot.set_dsc_poll()
    discord_bot.set_dsc_mod()
    discord_bot.set_dsc_give()

    #Sends a message to console when the bot is online
    @discord_bot.client.event
    async def on_ready():
      print(f'Bot online as {discord_bot.client.user}')
    #runs the discord bot
    discord_bot.client.run(secret_key)
  #Initialises dsc_vr and makes sure the file exists and has necessary dependencies stored inside it
  def set_dsc_vr():
    if not exists(discord_bot.dsc_vr+".db"):
      db = shelve.open(discord_bot.dsc_vr)
      db['secret_key'] = None
      db['cmd_prefix'] = None
      db['loop_status'] = False
      db['music_queue'] = []
      db['song_titles'] = []
      db.close()
    else:
      return
  #Initialise dsc_poll and make sure the file exists and has necessary dependencies stored inside it
  def set_dsc_poll():
    if not exists(discord_bot.dsc_poll+'.db'):
      db_poll = shelve.open(discord_bot.dsc_poll)
      db_poll['id_tracker'] = 0
      db_poll.close()
    else:
      return
  #Initialise dsc_give and make sure the file exists and has necessary dependencies stored inside it
  def set_dsc_give():
    if not exists(discord_bot.dsc_mod+'.db'):
      db_give = shelve.open(discord_bot.dsc_give)
      db_give.close()
    else:
      return
  #Initialise dsc_mod and make sure the file exists and has necessary dependencies stored inside it
  def set_dsc_mod():
    if not exists(discord_bot.dsc_mod+'.db'):
      db_mod = shelve.open(discord_bot.dsc_mod)
      db_mod['timeout_words'] = ['penis']
      db_mod['ban_words'] = []
      db_mod['auto_timeout_minutes'] = 5
      db_mod['user_timouts'] = []
      db_mod.close()
    else:
      return
  #Check if the first char of a message contains the cmd_prefix
  async def command_check(ctx):
    db = shelve.open(discord_bot.dsc_vr)
    cmd_prefix = db['cmd_prefix']
    db.close()
    if ctx.content[0] == cmd_prefix:
      return ctx.content[1:]
    else:
      return None




      