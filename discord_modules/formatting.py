'''
Formatting module

Finished:
-Handles message formatting and custom appearances for embedded messages

wip:
create module for adding buttons to messages with custom functionality
'''

import discord


#discord ebmedded module. Allows for discord embed messages to be sent in one line instead of several. Handles images, author, and reactions
async def dsc_embed(ctx, color=None, title=None, type='rich', url=None, description=None, timestamp=None, author = None, icon_url = None, reactions=None, ret = False, specific_channel = None):
  #embed object
  embed = discord.Embed(color=color,title=title,type=type,url=url,description=description,timestamp=timestamp)
  #if author is passed to the function sets the author of the embedded message
  if author:
    embed.set_author(author)
  #if icon is passed to the function sets the icon url to be put on the embedded message
  if icon_url:
    embed.set_image(url=icon_url)

  #sends the embedded message and stores the message object inside the variable message
  if not specific_channel:
    message = await ctx.channel.send(embed=embed)
  else:
    from . import discord_bot
    discord_bot.client.get_channel(specific_channel)

  #if reactions are passed to the function it loops through them and adds them to the message
  if reactions:
    for reaction in reactions:
      await message.add_reaction(reaction)
  if ret == True:
    return message