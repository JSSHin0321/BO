from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import datetime
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
    
    if not message.content.startswith(PREFIX):
        return
    
    parts = message.content.split()
    command = parts[0][len(PREFIX):]
    
    if command == '보스':
        boss_info_list = []
        for boss in boss_list.values():
            if boss['last_kill_time'] is None:
                expected_spawn_time = ''
            else:
                last_kill_time = datetime.datetime.strptime(boss['last_kill_time'], '%Y-%m-%d %H:%M:%S.%f')
                regen_time = datetime.timedelta(hours=int(boss['regen_time'][0]))
                expected_spawn_time = last_kill_time + regen_time
                expected_spawn_time = expected_spawn_time.strftime('%H:%M:%S')
            
            boss_info = f"{boss['name']} (Lv. {boss['level']})  {expected_spawn_time}"
            boss_info_list.append(boss_info)
        
        boss_info_str = "\n".join(boss_info_list)
        boss_embed = discord.Embed(title="보스 정보", description=boss_info_str, color=0x00FF00)
        await message.channel.send(embed=boss_embed)

    elif command in boss_list:
        boss = boss_list[command]
        if len(parts) == 1 or parts[1] == '컷':
            boss['last_kill_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            await message.channel.send(f"{boss['name']}의 last kill time이 갱신되었습니다.")
        elif parts[1].isdigit():
            hour = int(parts[1]) // 100
            minute = int(parts[1]) % 100
            now = datetime.datetime.now()
            boss['last_kill_time'] = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            await message.channel.send(f"{boss['name']}의 last kill time이 갱신되었습니다.")
        elif parts[1] == '초기화':
            boss['last_kill_time'] = None
            await message.channel.send(f"{boss['name']}의 last kill time이 초기화되었습니다.")




try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
