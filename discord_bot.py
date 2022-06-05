import discord
import sys
import time
import asyncio
from variables_interface import GlobalVariables, Messages
import time_parsing as tp

gv = GlobalVariables()
ms = Messages()

class Reminder():
    def __init__(self, user: discord.abc.User, channel, endtime: float, reason=None, typeR=None):
        self.user = user
        self.endtime = endtime
        self.reason = reason
        self.channel = channel
        self.typeR = typeR

    def __str__(self):
        return ms._reminder_object_str.format(self.user, round(self.endtime-time.time(),0), str("("+self.reason+")"))

    def isUp(self):
        if time.time() >= self.endtime:
            return True
        return False


class DiscordClient(discord.Client):
    async def bgReminders(self):
        while True:
            for i, reminder in enumerate(reminders):
                if reminder.isUp():
                    if reminder.typeR == 'channel':
                        message = ms.reminder_done_channel.format(reminder.user.id, reminder.reason)
                        await reminder.channel.send(message)
                    elif reminder.typeR == 'pm':
                        message = ms.reminder_done_pm.format(reminder.user.id, reminder.reason, reminder.channel.id)
                        await reminder.user.send(message)
                    reminders.pop(i)
            await asyncio.sleep(1)

    async def cmdHelp(message):
        channel = message.channel
        content = ""
        if gv.language == "fr":
            content = "**--- :robot: Commandes disponibles : ---**\n"
        else:
            content = "**--- :robot: Available commands : ---**\n"
        for command in COMMANDS:
            content += f"**:point_right: {str(command[0]).replace('(', '').replace(')', '')}** : {command[2]}\n"
        await channel.send(content)

    async def cmdRemindChanIn(message):
        endtime = await addReminder(message, 'channel')
        if endtime:
            await message.add_reaction('✅')
            await message.channel.send(ms.reminder_added_channel.format(f'<@{message.author.id}>', tp.getTimeDelta(endtime)))
        else:
            return None

    async def cmdRemindMeIn(message):
        endtime = await addReminder(message, 'pm')
        if endtime:
            await message.add_reaction('✅')
            await message.channel.send(ms.reminder_added_pm.format(f'<@{message.author.id}>', tp.getTimeDelta(endtime)))
        else:
            return None

    global reminders, COMMANDS
    reminders = list()
    # (Chat command, function to be called, description dictionary)
    COMMANDS = (
        # %help, %h, %?
        (
            (f'{gv.prefix}help', f'{gv.prefix}h', f'{gv.prefix}?'), 
            cmdHelp, ms.help_help
        ),
        # %remindchannelin, %remindchanin, %rcin
        (
            (f'{gv.prefix}remindchannelin', f'{gv.prefix}remindchanin', f'{gv.prefix}rcin'), 
            cmdRemindChanIn, ms.help_remindchannel
        ),
        # %remindmein, %rmin
        (
            (f'{gv.prefix}remindmein', f'{gv.prefix}rmin'), 
            cmdRemindMeIn, ms.help_remindme
        ),
        # %remindchannelat, %remindchanat, %rcat (WIP)
        # %remindmeat, %rmat (WIP)
    )

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print('[INFO] Set prefix is', gv.prefix)
        print('[INFO] Set language is', gv.language)
        rpc_name = "his stopwatch" if gv.prefix=='en' else "sa montre"
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=rpc_name))

    async def on_message(self, message):
        for command in COMMANDS:
            if message.content.startswith(command[0]):
                await command[1](message)
        return None

async def addReminder(message, typeR):
    channel = message.channel
    time_specified, reason = tp.extractInfoFromMessage(message)
    endtime = tp.messageToSeconds(time_specified)
    if endtime == -1:
        await channel.send(ms.reminder_error_invalid)
        return False
    else: # Time specified is valid            
        reminders.append(Reminder(message.author, message.channel, endtime, reason, typeR))
        return endtime