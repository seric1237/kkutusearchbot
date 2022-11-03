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
spreadsheet_key = os.environ['key']
doc = gc.open_by_key(spreadsheet_key)
sheet = doc.worksheet("시트1")
column_data = sheet.col_values(1)
update = list(set(column_data))


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
    
    spreadsheet_key = os.environ['key']
    doc = gc.open_by_key(spreadsheet_key)
    global sheet
    sheet = doc.worksheet("시트1")
    column_data = sheet.col_values(1)
    global update
    update = list(set(column_data))
    await ctx.send('업데이트 완료')


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
async def 단어추가(ctx):
    adw = ctx.message.content[6:]
    olw = []
    for i in update:
        if i == adw:
            olw.append(adw)
            break
    if len(olw) == 0:
        update.append(adw)
        sheet.append_row([adw])
        await ctx.send('단어 추가가 완료되었습니다')
    elif len(olw) == 1:
        await ctx.send('이미 있는 단어입니다')


@client.command()
async def 단어삭제(ctx):
    dlw = ctx.message.content[6:]
    srw = []
    for i in update:
        if i == dlw:
            srw.append(dlw)
            break
    if len(srw) == 0:
        await ctx.send('없는 단어입니다')
    elif len(srw) == 1:
        update.remove(dlw)
        dln = sheet.find(dlw)
        sheet.delete_rows(dln.row)
        await ctx.send('단어 삭제가 완료되었습니다')
    
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
    wnm = ctx.message.content[8:9]
    if len(wnm) > 0:
        for i in update:
            if i.rfind(sew) == len(i) - 1 and len(i) == int(wnm):
                search_result.append(i)
    else:
        for i in update:
            if i.rfind(sew) == len(i) - 1:
                search_result.append(i)
        search_result.sort(key=len, reverse=True)
    await ctx.send(search_result[0:5])

@client.command()
async def 앞말검색(ctx):
    search_result = []
    sfw = ctx.message.content[6:7]
    wnm = ctx.message.content[8:9]
    if len(wnm)>0:
        for i in update:
            if i.find(sfw) == 0 and len(i) == int(wnm):
                search_result.append(i)
    else:
        for i in update:
            if i.find(sfw) == 0:
                search_result.append(i)
        search_result.sort(key=len, reverse=True)
    await ctx.send(search_result[0:5])
   
@client.command()
async def 단어검색(ctx):
    search_result = []
    serw = ctx.message.content[6:]
    for i in update:
        if i.find(serw) > -1:
            search_result.append(i)
            
    search_result.sort(key=len)
    result = search_result[::-1]
    await ctx.send(result[0:5])


client.run(os.environ['token'])
