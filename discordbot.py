from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()


boss_list = {
    '제니나': {
        'name': '제니나',
        'level': 47,
        'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbS6EiX%2FbtsaibxQI5N%2FeL7dfmI4SnKL5hI6rDXurK%2Fimg.png',
        'regen_time': '3시간',
        'last_kill_time': None
    },
    '수호자': {
        'name': '수호자',
        'level': 47,
        'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbmjUmZ%2FbtsakfT1ktr%2FhSqjg4Pz9hKOkg3dYUJ540%2Fimg.png',
        'regen_time': '3시간',
        'last_kill_time': None
    }
}



@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == f'{PREFIX}보스':
        boss_names = [boss['name'] for boss in boss_list.values()]
        boss_list_str = "\n".join(boss_names)
        await message.channel.send(f"보스 리스트:\n{boss_list_str}")




try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
