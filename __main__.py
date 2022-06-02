import discord_bot as db
import variables_interface as v

if __name__ == '__main__':
    gv = v.GlobalVariables()
    client = db.DiscordClient()
    client.loop.create_task(client.bgReminders())
    client.run(gv.token)