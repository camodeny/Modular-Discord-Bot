'''
Poll module

finished:

wip:
-create_poll function
  -create a poll with a unique id
  -store poll data with id inside dsc_poll
  -add reactions
  -allow for yes/no or multiple answer poll types
  -send off to .formatting embed to have the embedded message and reactions sent off
'''

#import main class
from . import discord_bot
import shelve
from .formatting import dsc_embed

async def create_poll(ctx, title, description, reactions=[u"\U0001F44D",u"\U0001F44E"], type='yn', send_id=True, return_poll_obj=False, icon_url=None, specific_channel=None):
  db_poll = shelve.open(discord_bot.dsc_poll)
  if icon_url == None:
    poll_message_obj = await dsc_embed(ctx, title=title, description=description, reactions=reactions, ret = True)
  else:
    poll_message_obj = await dsc_embed(ctx, icon_url=icon_url, title=title, description=description, reactions=reactions, ret = True)

  db_poll['id_tracker'] += 1
  db_poll[str(db_poll['id_tracker'])] = {'poll_id': db_poll['id_tracker'], 'title': title, 'description': description, 'poll_message_id' : poll_message_obj.id}
  if send_id:
    await ctx.author.send(f'Poll {title} created\nPoll ID: {db_poll["id_tracker"]}')
  if return_poll_obj:
    db_poll.close()
    return poll_message_obj
  db_poll.close()
    