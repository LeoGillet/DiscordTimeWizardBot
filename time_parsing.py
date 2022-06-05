import time
from datetime import timedelta

def messageToSeconds(given_time):
    supported_chars = ('d', 'h', 'm', 's')
    start = 0
    words = list()
    for index, char in enumerate(given_time):
        try: 
            int(char)
        except ValueError:
            if char in supported_chars:
                print("Parsing", given_time[start:index])
                number = int(given_time[start:index])
                words.append({"number": number, "unit": char})
                start = index+1
            else:
                return -1

    endtime = time.time()
    for word in words:
        number = word["number"]
        unit = word["unit"]
        if unit == 's':
            endtime += number
        if unit == 'm':
            endtime += number*60
        if unit == 'h':
            endtime += number*3600
        if unit == 'd':
            endtime += number*86400
        
    return endtime


def extractInfoFromMessage(message):
    content = message.content.split()
    channel = message.channel
    author = message.author
    time_specified = content[1]
    reason = None
    if len(content) > 2:
        reason = ' '.join(content[2:])
    return time_specified, reason


def getTimeDelta(endtime):
    return timedelta(seconds=endtime-time.time())
