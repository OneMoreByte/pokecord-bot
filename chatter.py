#!/usr/bin/env python3

import discord
import os
import glob
import random
import asyncio
from datetime import datetime

client = discord.Client(max_messages=100,status=discord.Status.online,activity=discord.Game(name="the system."))


token = os.environ['TOKEN']
wake = float(os.environ['WAKE'])
sleep  = float(os.environ['SLEEP'])
wpm = int(os.environ['WPM'])


# Returns a random sleep time for simulated "thinking"
def get_sleeptime():
    return random.randint(5, 60)


# Returns time to type out the content in minutes
def get_typetime(txt):
    words = len(txt.split())
    return words * 60 / wpm


# Returns bool if time is past sleep time
def check_time():
    time = datetime.now()
    h = time.hour
    m = time.minute
    s = time.second
    floathour = float(h) + float(m/60) + float(s/3600) 
    waketime = (sleep + get_wake_time_delta()/3600)
    return floathour > sleep and floathour < waketime


# Returns time delta in seconds
def get_wake_time_delta():
    if sleep > wake:
        return (24 + wake - sleep) * 3600
    elif sleep < wake:
        return (wake - sleep) * 3600
    else:
        return 0


@client.event
async def on_ready():
# Load a movie script into the program
    async def load_rambling():
        files = glob.glob("/movies/*.txt")
        count = random.randint(0,len(files)-1)
        await debug("Saw {} dialog files. Choosing {} for the next 300 calls.".format(len(files), files[count]))
        with open(files[count]) as f:
            data = f.readlines()
        return data


    # Print random text
    async def ramble(data):
        txt = ""
        while txt.strip() is "":
            numb = random.randint(0,len(data)-1)
            txt = data[numb]
        async with activec.typing():
            await asyncio.sleep(get_typetime(txt))
            await activec.send(txt.strip())


    # Prints to #debug chat
    async def debug(output):
        timestamp = datetime.now()
        print("[{}]: {}".format(timestamp, output))


    print('Logged in as {0.user}'.format(client))
    server = client.get_guild('hard-coded server id')
    debugc = server.get_channel('hard-coded channel id for debuging')
    activec = server.get_channel('hard-coded channel id for activity')

    await debug("Started bot.")
    data = await load_rambling()
    cnt = 0
    print(len(data))
    await ramble(data)
    while(True):
        sleeping = True
        for u in server.get_role('hard coded group id').members:
            if u.status is discord.Status.online:
                sleeping = False

        if sleeping:
            await debug("Sleeping for five minute, no one online")
            await client.change_presence(status=discord.Status.idle,activity=discord.Game(name="the system."))
            await asyncio.sleep(60*5)
        else:
            await ramble(data)
            await asyncio.sleep(get_sleeptime())
            cnt += 1
            if cnt > 300:
                cnt = 0
                data = await load_rambling()
            if server.me.status is not discord.Status.online:
                await client.change_presence(status=discord.Status.online,activity=discord.Game(name="the system."))

                       

print("token={}\nwake={}\nsleep={}\nwpm={}".format(token, wake, sleep, wpm))
client.run(token, bot=False)
