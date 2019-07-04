from discord.ext import commands
import discord
import datetime

import urllib.request
import json

import config

from random import randrange

from library import sources

class Watch(commands.Cog):
    """Bot utilities regarding Watch functionality (watch for new content in channels such as youtube)."""
    def __init__(self, bot):
        self.bot = bot
        self.channels = []
        self.scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    @commands.group()
    async def seuraa(self, ctx):
        if ctx.invoked_subcommand is None:
            try:
                lista_message = f"Lista seuratuista kanavista: ?seuraa lista\n"
                embed = discord.Embed(colour=0xFF0000, title=f'Seuranta')
                embed.add_field(name='Lista', value=lista_message, inline=False)
                await ctx.send(embed=embed)
            except discord.Forbidden:
                await ctx.send("Ei oikeuksia.")

    @seuraa.group(name="lista")
    async def seuranta_list(self, ctx):
        """List channels we are following"""
        listed_channels = ""
        for channel in self.channels:
            listed_channels += f'{channel.name} \n'
        await ctx.send(listed_channels)

    @seuraa.group(name="lisaa")
    async def seuranta_add(self, ctx, name):
        """Add channel to follow list"""
        self.channels.append(sources.channel(name)) 
    
    @commands.command(hidden=True)
    async def testi(self, ctx):
        # Just an experiment to fetch list of videos from googleAPI for POC purposes
        api_key = config.dev_test_api_key
        base_video_url = "https://www.youtube.com/watch?v="
        base_search_url = "https://www.googleapis.com/youtube/v3/search?"

        first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key, config.dev_test_channel_id)

        video_links = []
        url = first_url
        while True:
            inp = urllib.request.urlopen(url)
            resp = json.load(inp)

            for i in resp['items']:
                if i['id']['kind'] == "youtube#video":
                    video_links.append(base_video_url + i['id']['videoId'])

            try:
                next_page_token = resp['nextPageToken']
                url = first_url + '&pageToken={}'.format(next_page_token)
            except:
                break
        print(video_links)

def setup(bot):
    bot.add_cog(Watch(bot))