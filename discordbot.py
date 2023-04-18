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


async def cut_command(message, boss_name):
    if boss_name not in boss_list:
        return

    boss = boss_list[boss_name]
    kill_time = message.created_at
    boss['last_kill_time'] = kill_time
    await message.channel.send(f'{boss_name} killed at {kill_time.strftime("%H:%M:%S")}.')

async def time_command(message, boss_name, kill_time_str):
    if boss_name not in boss_list:
        return

    boss = boss_list[boss_name]
    try:
        kill_time = datetime.datetime.strptime(kill_time_str, "%H%M")
        boss['last_kill_time'] = kill_time
        await message.channel.send(f'{boss_name} killed at {kill_time.strftime("%H:%M:%S")}.')
    except ValueError:
        await message.channel.send('Invalid time format. Please use the format "HHMM".')

async def boss_command(message):
    boss_list_str = "Boss List\n"
    sorted_bosses = sorted(boss_list.values(), key=lambda b: b['last_kill_time'] + datetime.timedelta(hours=int(b['regen_time'][:-2])) if b['last_kill_time'] else None)

    for b in sorted_bosses:
        if b['last_kill_time']:
            respawn_time = b['last_kill_time'] + datetime.timedelta(hours=int(b['regen_time'][:-2]))
            boss_list_str += f"{b['name']} (Lv. {b['level']}) => {respawn_time.strftime('%H:%M:%S')}\n"
        else:
            boss_list_str += f"{b['name']} (Lv. {b['level']}) => No kill history\n"

    await message.channel.send(boss_list_str)

async def reset_command(message, boss_name):
    if boss_name not in boss_list:
        return

    boss = boss_list[boss_name]
    boss['last_kill_time'] = None
    await message.channel.send(f'{boss_name} kill history has been reset.')

COMMANDS = {
    '컷': cut_command,
    '시간': time_command,
    '보스': boss_command,
    '초기화': reset_command
}

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.split()
    if len(content) < 2:
        return

    boss_name, command = content[:2]
    if command in COMMANDS:
        await COMMANDS[command](message, boss_name, *content[2:])

        
        
        
        
        
try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
