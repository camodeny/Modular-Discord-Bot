'''
Giveaway Module

Finished:

wip:
-Create function to create giveaways
-Add poll variant
-Add discord invite variant
'''

from . import discord_class
import shelve

async def create_giveaway(ctx, title, description, time, type='poll', icon_url=None, specific_channel = None):
  if type='poll':
    from .poll import create_poll
    giveaway = create_poll(ctx, title, description, send_id=False, return_poll_obj=True, specific_channel=specific_channel, icon_url=icon_url)
    db_give = shelve.open(discord_class.dsc_give)
    poll_details = {'reactions':None, 'message_id':giveaway.id}
  elif type='invite':
    from .formatting import dsc_embed
    if icon_url == None:
      dsc_embed(ctx, title, description, ret=True, specific_channel=specific_channel)
