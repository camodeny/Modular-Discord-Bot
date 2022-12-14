from discord_modules import discord_bot
from discord_modules.moderating import auto_timeout


@discord_bot.client.event
async def on_message(ctx):
  if not ctx.author == discord_bot.client.user:
    command = await discord_bot.command_check(ctx)
    if command:
      command = command.split(" ")


      #poll command
      if command[0] == "poll":
        from discord_modules.poll import create_poll
        if command[1] == 'yn':
          await create_poll(ctx, command[2], command[3])




      ###############
      #Music Commands

      #join voice channel command
      elif command[0] == "joinvc":
        from discord_modules.music import join_voice
        if (len(command) == 2):
          await join_voice(ctx, command[1])
        elif (len(command) == 1):
          await join_voice(ctx)

      #leave voice channel command
      elif command[0] == 'leavevc':
        from discord_modules.music import leave_voice
        await leave_voice(ctx)

      #song request command
      elif command[0] == "sr":
        from discord_modules.music import song_request
        await song_request(ctx, command)

      #play command
      elif command[0] == "play":
        from discord_modules.music import play
        await play(ctx)

      #pause command
      elif command[0] == "pause":
        from discord_modules.music import pause
        await pause(ctx)

      #resume command
      elif command[0] == "resume":
        from discord_modules.music import resume
        await resume(ctx)

      #next command
      elif command[0] == "next":
        from discord_modules.music import next_song
        await next_song(ctx)

      #remove from queue command
      elif command[0] == "remove":
        from discord_modules.music import remove_queue
        await remove_queue(ctx, command[1])

      #previous command
      elif command[0] == "previous":
        from discord_modules.music import previous
        await previous(ctx)



      #Unable to recognize command statement
      else:
        confused_string = "I'm sorry I don't understand "
        for x in command:
          confused_string += " " + str(x)

    #automod
    if not command:      
      await auto_timeout(ctx)

discord_bot.__init_bot__()