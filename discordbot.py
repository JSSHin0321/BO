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
        elif message.content.startswith(f"{boss_name} "):
            input_time_str = message.content.split(' ')[1]
            await boss_kill(message, boss_name, input_time_str)

async def boss_kill(message, boss_name, input_time_str=None):
    tz = pytz.timezone('Asia/Seoul')
    now = datetime.datetime.now(tz)

    if input_time_str is None:
        kill_time = now
    else:
        try:
            input_time = datetime.datetime.strptime(input_time_str, '%H%M')
        except ValueError:
            await message.channel.send(f"{boss_name} : 입력한 시간이 유효하지 않습니다.")
            return

        kill_time = datetime.datetime(now.year, now.month, now.day, input_time.hour, input_time.minute, tzinfo=tz)

        if now >= kill_time:
            kill_time += datetime.timedelta(days=1)

    regen_time = kill_time + datetime.timedelta(hours=3)
    regen_time_str = regen_time.strftime("%H:%M:%S")

    boss_list[boss_name]['last_kill_time'] = kill_time

    await message.channel.send(f"{boss_name} Kill. {boss_name}는 {regen_time_str}에 다시 출현합니다.")

    # Update boss list
    await print_boss_list(message)




async def print_boss_list(message):
    sorted_boss_list = sorted(boss_list.values(), key=lambda x: x['last_kill_time'] + datetime.timedelta(hours=3) if x['last_kill_time'] else datetime.datetime.max)
    boss_list_str = "```보스 리스트:\n"
    for boss in sorted_boss_list:
        next_spawn_time_str = " "
        if boss['last_kill_time']:
            next_spawn_time = boss['last_kill_time'] + datetime.timedelta(hours=3)
            next_spawn_time_str = next_spawn_time.strftime("%H:%M:%S")
        boss_list_str += f"{boss['name']} (Lv. {boss['level']}) => {next_spawn_time_str}\n"
    boss_list_str += "```"
    await message.channel.send(boss_list_str)









try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
