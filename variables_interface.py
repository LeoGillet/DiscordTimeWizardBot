import json

class Messages():
    def __init__(self):
        file = json.load(open("variables.json", encoding='utf-8'))
        self.language = file["language"]
        self.hours = file["words"]["hours"][self.language]
        self.seconds = file["words"]["seconds"][self.language]
        self.reminder_added_channel = file["messages"]["reminder_added_channel"][self.language]
        self.reminder_added_pm = file["messages"]["reminder_added_pm"][self.language]
        self.reminder_error_numerical = file["messages"]["reminder_error_numerical"][self.language]
        self.reminder_error_unit = file["messages"]["reminder_error_unit"][self.language]
        self.reminder_error_unknown = file["messages"]["reminder_error_unknown"][self.language]
        self.reminder_done_channel = file["messages"]["reminder_done_channel"][self.language]
        self.reminder_done_pm = file["messages"]["reminder_done_pm"][self.language]
        self._reminder_object_str = file["messages"]["_reminder_object_str"][self.language]
        self.help_help = file["messages"]["help_help"][self.language]
        self.help_remindchannel = file["messages"]["help_remindchannel"][self.language]
        self.help_remindme = file["messages"]["help_remindme"][self.language]

class GlobalVariables():
    def __init__(self):
        file = json.load(open("variables.json", encoding='utf-8'))
        secret = json.load(open("secret_variables.json"))
        self.token = secret["token"]
        self.channels = secret["channels"]
        self.prefix = file["prefix"]
        self.language = file["language"]

    def updateJSON(self):
        values = {"token": self.token, "channels": self.channels, "prefix": self.prefix}
        jsonOBJ = json.dumps(values, indent=4)
        with open("variables.json", "w") as newfile:
            newfile.write(jsonOBJ)

    def setPrefix(self, new_prefix):
        if new_prefix in ('%', 'µ', '€', '&', '§', '!', '<', '>', 'ù'):
            self.prefix = new_prefix
            self.updateJSON()
            print("[INFO] Prefix has been set to {}".format(new_prefix))
            return True
        else:
            print("[WARN] Prefix cannot be set to {}".format(new_prefix))
            return False
    
    def addChannel(self, channel_id):
        self.channels.append(channel_id)
        self.updateJSON()
