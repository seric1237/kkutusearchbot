from discord.ext import commands
import pandas as pd
import random
import numpy as np
import discord
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

json_key_path = "key.json" # JSON Key File Path
credential = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
gc = gspread.authorize(credential)

spreadsheet_key = "1MmD-THB63KkhYsSxUnu7iWuL8K0wMdfibzIAM3OitWk"
doc = gc.open_by_key(spreadsheet_key)
sheet = doc.worksheet("시트1")
temp = sheet.get_all_values()
update = list(set(temp))


client = commands.Bot(command_prefix='!', intents=discord.Intents.all())



@client.event
async def on_ready():
    print('{} logged in.'.format(client))
    print('Bot: {}'.format(client.user))
    print('Bot name: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    

@client.command()
async def 업데이트(ctx):
    scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
    ]

    json_key_path = "key.json" # JSON Key File Path
    credential = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
    gc = gspread.authorize(credential)
    
    spreadsheet_key = "1MmD-THB63KkhYsSxUnu7iWuL8K0wMdfibzIAM3OitWk"
    doc = gc.open_by_key(spreadsheet_key)
    sheet = doc.worksheet("시트1")
    temp = sheet.get_all_values()
    update = list(set(temp))


@client.command()
async def 미션검색(ctx):
    sfw = ctx.message.content[6:7]
    smw = ctx.message.content[8:9]
    mission_len = []
    mission_search = []
    mss = []
    for word in update:
        c = word.count(smw)
        if c > 0 and word.find(sfw) == 0:
            mission_len.append(c)
            mission_search.append(word)
    mission = np.array(mission_search)
    mission_len_array = np.array(mission_len)
    sorting_index = np.argsort(mission_len_array)
    mission_result = mission[sorting_index]
    a = mission_result[::-1]
    result = a.tolist()
    n = result[0].count(smw)
    for word in update:
        c = word.count(smw)
        if c == n and word.find(sfw) == 0:
            mss.append(word)
    mss.sort(key=len, reverse=True)
    await ctx.send('{}미 {}'.format(n, mss[0:5]))


@client.command()
async def 미션개수(ctx):
    sfw = ctx.message.content[6:7]
    smw = ctx.message.content[8:9]
    num = ctx.message.content[10:11]
    mission_search = []

    for word in update:
        c = str(word.count(smw))
        if c == num and word.find(sfw) == 0:
            mission_search.append(word)
    mission_search.sort(key=len)
    result = mission_search[::-1]
    await ctx.send(result[0:5])

@client.command()
async def 빌런검색(ctx):
    search_result = []
    sfw = ctx.message.content[6:7]
    sew = ctx.message.content[8:9]
    for i in update:
        if i.find(sfw) == 0 and i.find(sew, len(i) - 1) == len(i) - 1:
            search_result.append(i)

    search_result.sort(key=len)
    result = search_result[::-1]
    await ctx.send(result[0:5])

@client.command()
async def 끝말검색(ctx):
    search_result = []
    sew = ctx.message.content[6:7]
    for i in update:
        if i.find(sew) == len(i) - 1:
            search_result.append(i)

    search_result.sort(key=len)
    result = search_result[::-1]
    await ctx.send(result[0:5])

@client.command()
async def 앞말검색(ctx):
    search_result = []
    sfw = ctx.message.content[6:7]
    for i in update:
        if i.find(sfw) == 0:
            search_result.append(i)

    search_result.sort(key=len)
    result = search_result[::-1]
    await ctx.send(result[0:5])


client.run(os.environ['token'])
