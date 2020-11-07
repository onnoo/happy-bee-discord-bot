import json
import os
from urllib import parse
import discord
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
bot_token = os.environ['BOT_TOKEN']
riot_token = os.environ['X_RIOT_TOKEN']


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


@bot.command(name="소환사")
async def search(ctx, *, summoner_name):

    # Summoner
    enc_summoner_name = parse.quote(summoner_name)
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{enc_summoner_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.4240.111 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": riot_token
    }
    summoner = json.loads(requests.get(url=url, headers=headers).text)

    # League
    summoner_id = summoner['id']
    url = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    leagues = json.loads(requests.get(url=url, headers=headers).text)
    league = [i for i in leagues if i['queueType'] == "RANKED_SOLO_5x5"][0]
    total_games = league['wins'] + league['losses']
    win_rate = league['wins'] / total_games * 100

    if "miniSeries" in league:
        p_dict = {'N': '-', 'W': 'O', 'L': 'X'}
        mini_desc = "\n승급전: " + "".join([p_dict[p] for p in league['miniSeries']['progress']])
    else:
        mini_desc = ""

    # Build embed
    title = f"{league['tier']} {league['rank']} - {league['leaguePoints']}점"
    description = f"{total_games}전 {league['wins']}승 {league['losses']}패 ({win_rate:.2f}%){mini_desc}"

    author_name = f"{summoner['name']} (LV. {summoner['summonerLevel']})"
    author_icon_url = f"http://ddragon.leagueoflegends.com/cdn/10.22.1/img/profileicon/{summoner['profileIconId']}.png"

    thumbnail_url = f"http://z.fow.kr/img/emblem/{league['tier'].lower()}.png"

    embed = discord.Embed(title=title, description=description, color=0xffa62b)
    embed.set_author(name=author_name, icon_url=author_icon_url)
    embed.set_thumbnail(url=thumbnail_url)
    await ctx.send(embed=embed)

if __name__ == '__main__':
    bot.run(bot_token)
    # Temp
