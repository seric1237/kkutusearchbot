from discord.ext import commands
import pandas as pd
import random
import numpy as np
import discord
import os
Location = 'C:\kkutu'
ao = 'kkutu_integrated.xlsx'
column = 0

data_pd = pd.read_excel('{}/{}'.format(Location, ao), header=None, index_col=None, names=None)
data_np = pd.DataFrame.to_numpy(data_pd)

r = list(range(0, 290888))
pgd_list = []
for i in r:
    pgd_list.append(str(data_np[i][column]))

client = commands.Bot(command_prefix='!')




@client.event
async def on_ready():
    print('{} logged in.'.format(client))
    print('Bot: {}'.format(client.user))
    print('Bot name: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))


@client.command()
async def 미션검색(ctx):
    sfw = ctx.message.content[6:7]
    smw = ctx.message.content[8:9]
    mission_len = []
    mission_search = []
    mss = []
    for word in pgd_list:
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
    for word in pgd_list:
        c = word.count(smw)
        if c == n and word.find(sfw) == 0:
            mss.append(word)
    mss.sort(key=len, reverse=True)
    await ctx.send('{}미 {}'.format(n, mss[0:5]))


@client.command()
async def 미션갯수(ctx):
    sfw = ctx.message.content[6:7]
    smw = ctx.message.content[8:9]
    num = ctx.message.content[10:11]
    mission_search = []

    for word in pgd_list:
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
    for i in pgd_list:
        if i.find(sfw) == 0 and i.find(sew, len(i) - 1) == len(i) - 1:
            search_result.append(i)

    search_result.sort(key=len)
    result = search_result[::-1]
    await ctx.send(result[0:5])

@client.command()
async def 끝말검색(ctx):
    search_result = []
    sew = ctx.message.content[6:7]
    for i in pgd_list:
        if i.find(sew) == len(i) - 1:
            search_result.append(i)

    search_result.sort(key=len)
    result = search_result[::-1]
    await ctx.send(result[0:5])

@client.command()
async def 앞말검색(ctx):
    search_result = []
    sfw = ctx.message.content[6:7]
    for i in pgd_list:
        if i.find(sfw) == 0:
            search_result.append(i)

    search_result.sort(key=len)
    result = search_result[::-1]
    await ctx.send(result[0:5])


client.run(os.environ['token'])
