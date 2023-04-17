from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import datetime
import pytz

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
async def on_message(message):
    if message.author == client.user:
        return
        
    if message.content == '보스':
        await print_boss_list(message)
        
    for boss_name in boss_list.keys():
        if message.content == f"{boss_name} 컷":
            await boss_kill(message, boss_name)

async def boss_kill(message, boss_name):
    tz = pytz.timezone('Asia/Seoul')
    regen_time = datetime.datetime.now(tz) + datetime.timedelta(hours=3)
    regen_time_str = regen_time.strftime("%H:%M:%S")
    
    boss_list[boss_name]['last_kill_time'] = regen_time
    
    await message.channel.send(f"{boss_name} Kill. {boss_name}는 {regen_time_str}에 다시 출현합니다.")


async def print_boss_list(message):
    boss_list_str = "보스 리스트:\n"
    for boss in boss_list.values():
        last_kill_time_str = " "
        if boss['last_kill_time']:
            last_kill_time_str = boss['last_kill_time'].strftime("%H:%M:%S")
        boss_list_str += f"{boss['name']} (Lv. {boss['level']}) => {last_kill_time_str}\n"
    await message.channel.send(boss_list_str)




try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
