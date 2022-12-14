'''
Moderating module

Finished:
-auto timeout function

wip:
-ban function
-manual timeout
-custom reporting for moderators
-ability to make or grab existing moderator and admin roles
'''


import shelve
from . import discord_bot
import datetime

async def auto_timeout(ctx, message = False, channel_logs = False):
  db_mod = shelve.open(discord_bot.dsc_mod)
  for timeout_word in db_mod['timeout_words']:
    if timeout_word in ctx.content.lower():
      await ctx.author.timeout(datetime.timedelta(minutes=5), reason=(f'Auto moderator recognized {timeout_word} in the message {ctx.content} from {ctx.author}'))
      await ctx.delete()
  user_timeouts = db_mod['user_timeouts']
  user_timeouts.append({'author_id':ctx.author.id, 'author_name':ctx.author.name, 'reason':'Auto moderator timout for use of illegal words', 'evidence':ctx.content, 'reporter':'auto moderator'})
  db_mod['user_timeouts'] = user_timeouts
  db_mod.close()
  if message:
    await ctx.channel.send(f"{ctx.author}, you have been timed out for using unauthorized language. Your timeout is for 5 minutes")
  if channel_logs:
    from .formatting import 

async def add_timeout_words(words):
  db_mod = shelve.open(discord_bot.dsc_mod)
  timeout = db_mod['timeout_words']
  for word in words:
    timeout.append(word)
  db_mod['timeout_words'] = timeout




'''async def manual_timeout(ctx, command, timout_user, reason, evidence, time='5', delete_message = False, message = False`):
  db_mod = shelve.open(discord_bot.dsc_mod)
  tmp = command[1].split("@")
  tmp = tmp[1][:-1]
  command[1] = tmp
  try:
    user = ctx.guild.get_member(int(command[1]))
    await user.timeout(datetime.timedelta(minutes=int(time)), reason=(reason))
    user_timeouts = db_mod['user_timeouts']
    user_timeouts.append({'author_id':user.id,'author_name':user.name, 'reason':reason, 'evidence':evidence, 'reporter':ctx.author})
    if delete_message:
      ctx.delete()
    if message:
      await ctx.channel.send(f"{tmp} has been timed out for {time} minutes.")
  except:
    await ctx.channel.send("Unable to find the user requested. Either the user isn't in the server, or they haven't sent a message yet.")'''

async def mod_logs(ctx, ):