import discord
import sys
import time
import asyncio
from variables_interface import GlobalVariables, Messages

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
            content += f"**:point_right: {str(command[0]).replace('(', '').replace(')', '')}** : {command[2][gv.language]}\n"
        await channel.send(content)

    async def cmdRemindChan(message):
        endtime = await addReminder(message, 'channel')
        if endtime:
            await message.add_reaction('✅')
            await message.channel.send(ms.reminder_added_channel.format(f'<@{message.author.id}>', endtime[1], endtime[2]))
        else:
            return None

    async def cmdRemindMe(message):
        endtime = await addReminder(message, 'pm')
        if endtime:
            await message.add_reaction('✅')
            await message.channel.send(ms.reminder_added_pm.format(f'<@{message.author.id}>', endtime[1], endtime[2]))
        else:
            return None

    
    global reminders, COMMANDS
    reminders = list()
    # (Chat command, function to be called, description dictionary)
    COMMANDS = (
        # %help, %h, %?
        (
            (f'{gv.prefix}help', f'{gv.prefix}h', f'{gv.prefix}?'), 
            cmdHelp, 
            {
                "en": "Lists available commands and their description",
                "fr": "Liste les différentes commandes et leur description"
            }
        ),
        # %remindchannel, %rc
        (
            (f'{gv.prefix}remindchannel', f'{gv.prefix}remindchan', f'{gv.prefix}rc'), 
            cmdRemindChan,
            {
                "en":   "Reminds the user of doing something via a ping in the channel\n\t"+
                        "*Example : '%remindchan 30m Oven*' | '%rc 2h Fetch Bob from school'",
                "fr":   "Rappelle l'utilisateur d'une tâche à effectuer avec un ping dans le channel. Utilisation: %remindchan <durée> <raison>\n\t"+
                        "*Exemple : '%remindchan 30m Four*' | '%rc 2h Aller chercher Félix à l'école'"
            }
        ),
        (
            (f'{gv.prefix}remindme', f'{gv.prefix}rm'), 
            cmdRemindMe,
            {
                "en":   "Reminds the user of doing something via a private message\n\t"+
                        "*Example : '%remindme 30m Oven*' | '%rm 2h Fetch Bob from school'",
                "fr":   "Rappelle l'utilisateur d'une tâche à effectuer avec un message privé. Utilisation: %remindme <durée> <raison>\n\t"+
                        "*Exemple : '%remindme 30m Four*' | '%rm 2h Aller chercher Félix à l'école'"
            }
        )
    )

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print('[INFO] Set prefix is', gv.prefix)
        print('[INFO] Set language is', gv.language)

    async def on_message(self, message):
        if str(message.channel.id) in gv.channels:
            for command in COMMANDS:
                if message.content.startswith(command[0]):
                    await command[1](message)
            return None



def checkIfTimeValid(time_specified):
    try: # Checks if time is a numerical value
        num = int(time_specified[:-1])
    except:
        return -1
    
    if time_specified.endswith("h"):
        return time.time()+num*3600.0, num, ms.hours
    elif time_specified.endswith("m"):
        return time.time()+num*60.0, num, "minutes"
    elif time_specified.endswith("s"):
        return time.time()+num, num, ms.seconds
    else: # Unit is not valid
        return -2

async def addReminder(message, typeR):
    content = message.content.split()
    content.pop(0)
    channel = message.channel
    author = message.author
    time_specified = content[0]
    reason = None
    if len(content) > 1:
        reason = ' '.join(content[1:])
    endtime = checkIfTimeValid(time_specified)
    if endtime[0] > 0: # Time specified is valid            
        reminders.append(Reminder(author, channel, endtime[0], reason, typeR))
        return endtime
    else:
        if endtime == -1:
            await channel.send(ms.reminder_error_numerical)
        elif endtime == -2:
            await channel.send(ms.reminder_error_unit)
        else:
            await channel.send(ms.reminder_error_unknown)
        return False
