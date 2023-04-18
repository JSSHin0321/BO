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
        'spawn_time': None # 'regen_time' -> 'spawn_time' 으로 변경
    },
    '수호자': {
        'name': '수호자',
        'level': 47,
        'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbmjUmZ%2FbtsakfT1ktr%2FhSqjg4Pz9hKOkg3dYUJ540%2Fimg.png',
        'spawn_time': None # 'regen_time' -> 'spawn_time' 으로 변경
    }
}


async def boss_kill(message, boss_name, input_time_str=None):
    tz = pytz.timezone('Asia/Seoul')
    now = datetime.datetime.now(tz)

    if input_time_str is None:
        spawn_time = now
    else:
        try:
            input_time = datetime.datetime.strptime(input_time_str, '%H%M')
        except ValueError:
            await message.channel.send(f"{boss_name} : 입력한 시간이 유효하지 않습니다.")
            return

        spawn_time = datetime.datetime(now.year, now.month, now.day, input_time.hour, input_time.minute, tzinfo=tz)

        if now >= spawn_time:
            spawn_time += datetime.timedelta(days=1)

    boss_list[boss_name]['spawn_time'] = spawn_time

    await message.channel.send(f"{boss_name} Kill. {boss_name}는 {spawn_time.strftime('%H:%M:%S')}에 다시 출현합니다.")

    # Update boss list
    await print_boss_list(message)


async def print_boss_list(message):
    sorted_boss_list = await sort_bosses_by_spawn_time()

    boss_list_str = "```Boss List:\n"
    for boss_name, boss_info in sorted_boss_list.items():
        spawn_time_str = boss_info['spawn_time'].strftime("%H:%M:%S") if boss_info['spawn_time'] else " "
        boss_list_str += f"{boss_name} (Lv. {boss_info['level']}) => {spawn_time_str}\n"
    boss_list_str += "```"
    await message.channel.send(boss_list_str)


async def sort_bosses_by_spawn_time():
    tz = pytz.timezone('Asia/Seoul')
    now = datetime.datetime.now(tz)

    # Create a list of tuples that contains the boss name and the expected time of appearance
    bosses_with_spawn_time = []
    for boss_name, boss_info in boss_list.items():
        if boss_info['spawn_time']:
            spawn_time = boss_info['spawn_time']
        else:
            # Assign a very large estimated time to bosses without a spawn time
            spawn_time = now + datetime.timedelta(days=365)

        bosses_with_spawn_time.append((boss_name, spawn_time))

    # Sort the list of tuples based on the estimated time of appearance
    bosses_with_spawn_time.sort(key=lambda x: x[1])

    # Create a new dictionary that contains the sorted bosses
    sorted_boss_list = {}
    for boss_name, _ in bosses_with_spawn_time:
        sorted_boss_list[boss_name] = boss_list[boss_name]

    return sorted_boss_list


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


try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")







try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
