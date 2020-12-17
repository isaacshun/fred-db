#packages
import discord
from discord.ext import commands 
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
from fredapi import Fred
import seaborn as sns
fred = Fred(api_key = '60f66c4a9f6d11c8fe0834992f2a12a9')
#command prefix
client = commands.Bot(command_prefix = 'f ')
client.remove_command('help')

#Start up client event
@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(status = discord.Status.online, activity=discord.Game('Money go brrr'))

@client.command()
async def help(ctx):
    embed = discord.Embed(title = f"Hi there!", description = 'Here are the commands:', color = discord.Color.orange())
    embed.set_image(url='https://play-lh.googleusercontent.com/PaiehvTCBiycq_B8zdflQNSOE6i5kO5KzguquD-JMJwYKRYZEOwhAsQbgoC2524X13A')
    embed.add_field(name = 'plot', value = "Retrieves economical data from the Federal Reserve Economic Data (FRED) database and graphs it. Insert the short form of the data desired. If you don't know the short form, use the search function to search for the shortform", inline=False)
    embed.add_field(name = 'help', value = "Shows what you are seeing right now. Whenever you have questions, please use the help function", inline = False)
    embed.add_field(name = 'info', value = "Explains the information thoroughly, whenever you don't understand what the data does, this will be your go to function. Use the short form of the economic data.", inline = False)
    embed.add_field(name = 'search', value = 'Provides the short forms and full names of the top six search results in the FRED database. Whenever you forget or do not know the short form of the economic data, this is where you get your answer. To search, use double quotation marks (Example: "US inflation") around what you want to search. Please be as specific as possible, and try not to use only one word for searching. For example, instead of searching "GDP", search for a specific country or potential GDP', inline = False)
    embed.add_field(name = 'comp', value = "compare between two economic data retrieved from FRED. Adding split in the end will split the data graphs", inline = False)
    embed.add_field(name = 'stats', value = "summarizes the economic data retrieved from FRED to a box. With data from the most recent value to percent changes from time periods.", inline = False)
    embed.add_field(name = 'linreg', value = "This is the linear regression function, where you can use an independent variable to forecast the dependant variable using the least-squares simple linear regression method. This function uses the economic data shortform such as 'SP500' or 'NROU'. This function only allows one independent variable and one dependent variable. Note that some regression lines may be inaccurate, so make sure to analyze the data thoroughly. If the data cannot be forecasted, it's because the amount of data available between the two data is way too big", inline=False)
    embed.set_footer(text = 'Powered by FRED API')
    await ctx.send(embed = embed)

#client command
@client.command(aliases = ['ping'], brief = "Checks latency of bot")
async def latency(ctx):
    await ctx.send(f'Latency: {round(client.latency * 1000)}ms')

@client.command(brief = "stops the bot")
async def stop(ctx):
    await client.logout()

@client.command(brief = "plots economic data from the FRED database")
async def plot(ctx, series):
    try:
        data = fred.get_series(series)
        info = fred.get_series_info(series)
        title = info['title']
        sns.set_style("darkgrid")
        plt.plot(data)
        plt.title(title)
        plt.savefig(fname='plot')
        await ctx.send(file = discord.File('plot.png'))
        await ctx.send(f"Current value: {data[-1]}")
        plt.clf()
    except:
        await ctx.send("Sorry, the data does not exist, please try again")

@client.command(aliases=['comp'], brief = "compares between two economic data from the FRED database")
async def compare(ctx, series, series2, split = ''):
    try:
        data = fred.get_series(series)
        data2 = fred.get_series(series2)
        info = fred.get_series_info(series)
        info2 = fred.get_series_info(series2)
        if split == 'split':
            sns.set_style("darkgrid")
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.suptitle(f"Comparison between {info['title']} ({info['id']}) and {info2['title']} ({info2['id']})")
            ax1.plot(data)
            ax1.set_title(info['id'])
            ax2.plot(data2)
            ax2.set_title(info2['id'])
            plt.savefig(fname='plot')
            await ctx.send(file = discord.File('plot.png'))
            plt.clf()
        else:
            sns.set_style("darkgrid")
            plt.plot(data)
            plt.plot(data2)
            plt.legend([info['id'], info2['id']])
            plt.title(f"Comparison between {info['title']} ({info['id']}) and {info2['title']} ({info2['id']})")
            plt.savefig(fname='plot')
            await ctx.send(file = discord.File('plot.png'))
            plt.clf()
    except:
        await ctx.send("Sorry, the data does not exist, please try again")

@client.command(brief = "provides info of the economic data")
async def info(ctx, series):
    try:
        s_info = fred.get_series_info(series)
        sf_embed = discord.Embed(
            title = s_info['title'],
            description = s_info['notes'],
            colour = discord.Colour.blue()
        )
        await ctx.send(embed = sf_embed)
    except:
        await ctx.send("Sorry, the data does not exist, please try again")

@client.command(brief = "provides info of the economic data")
async def search(ctx, ticker):
    try:
        data = fred.search(ticker)
        sr_embed = discord.Embed(title = "Search Results", description = '',colour = 0x00ff00)
        sr_embed.add_field(name=data['title'][0],value=data['id'][0],inline=False)
        sr_embed.add_field(name=data['title'][1],value=data['id'][1],inline=False)
        sr_embed.add_field(name=data['title'][2],value=data['id'][2],inline=False)
        sr_embed.add_field(name=data['title'][3],value=data['id'][3],inline=False)
        sr_embed.add_field(name=data['title'][4],value=data['id'][4],inline=False)
        await ctx.send(embed = sr_embed)
    except:
        await ctx.send("Sorry, there are no search results avalible")

@client.command(brief = 'Provide statistics of the economic data')
async def stats(ctx, ticker):
    try:
        data = fred.get_series(ticker)
        data_info = fred.get_series_info(ticker)
        ot = (data[-1]-data[0])/data[0]

        embed = discord.Embed(
            title = data_info['title'],
            description = f"Popularity: {data_info['popularity']}",
            colour = discord.Colour.purple())
        embed.set_footer(text='Powered by FRED API')
        embed.add_field(name="Seasonal Adjustment", value = f" {data_info['seasonal_adjustment']}")
        embed.add_field(name = 'Frequency', value = f"{data_info['frequency']}", inline=False)
        embed.add_field(name="Last Observation", value = f" {data_info['observation_end']}", inline=False)
        embed.add_field(name = 'Last Observed price/value', value = f"{data[-1]}")
        embed.add_field(name = 'Change from previous observed price/value', value = f"{round((((data[-1] - data[-2])/data[-2])*100), 4)}%", inline = False)
        embed.add_field(name = 'Change Overtime', value = f"OverTime:     {round(ot*100,4)}%", inline = False)

        await ctx.send(embed = embed)
    except:
        await ctx.send("Sorry, there are no statistical results avalible")

@client.command(brief = "Provides Linear Regression Analysis")
async def linreg(ctx, df1, df2):
    try:
        data = fred.get_series(df1)
        data2 = fred.get_series(df2)
        info = fred.get_series_info(df1)
        info2 = fred.get_series_info(df2)
        data = data.fillna(method = 'backfill')
        data2 = data2.fillna(method = 'backfill')
        sns.set_theme(style = "darkgrid")
        sns.regplot(x = data, y = data2)
        plt.title(label = "Least-Squared Simple Regression")
        plt.xlabel(info['id'])
        plt.ylabel(info2['id'])
        plt.savefig(fname='plot')
        await ctx.send(file = discord.File('plot.png'))
        plt.clf()
    except:
        await ctx.send("Sorry, the data cannot be forecasted, please try again")

    

#Client token
TOKEN = 'Nzg4MDc1MDIyNDQ2MjMxNTcy.X9eODw.Sg-0s1WaMfIGLl-dN1JKuwgJMX0'
client.run(TOKEN)
