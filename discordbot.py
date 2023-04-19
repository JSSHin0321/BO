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
    
    if message.content.startswith(f'{PREFIX}보스 '):
        command = message.content.split(' ')
        if len(command) == 2:
            boss_name = command[1]
            if boss_name in boss_list:
                if command[0] == '컷':
                    boss_list[boss_name]['last_kill_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                    await message.channel.send(f"{boss_name} 컷 기록 완료.")
                elif command[0].isdigit():
                    boss_list[boss_name]['last_kill_time'] = datetime.datetime.now().strftime('%Y-%m-%d ') + command[0][:2] + ':' + command[0][2:] + ':00.000000'
                    await message.channel.send(f"{boss_name} {command[0]} 기록 완료.")
                else:
                    await message.channel.send("올바른 명령어를 입력해주세요.")
            else:
                await message.channel.send("해당 보스가 존재하지 않습니다.")
        elif message.content == f'{PREFIX}보스':
            boss_embed = discord.Embed(title="보스 정보", color=0x00FF00)
            boss_embed.set_thumbnail(url="<BOSS THUMBNAIL URL>")
            for boss in boss_list.values():
                if boss['last_kill_time'] is None:
                    expected_spawn_time = ''
                else:
                    last_kill_time = datetime.datetime.strptime(boss['last_kill_time'], '%Y-%m-%d %H:%M:%S.%f')
                    regen_time = datetime.timedelta(hours=int(boss['regen_time'][0]))
                    expected_spawn_time = last_kill_time + regen_time
                    expected_spawn_time = expected_spawn_time.strftime('%H:%M:%S')
                
                boss_embed.add_field(name=f"{boss['name']} (Lv. {boss['level']})", value=f"예상 출현 시간: {expected_spawn_time}", inline=False)
            
            await message.channel.send(embed=boss_embed)
        else:
            await message.channel.send("올바른 명령어를 입력해주세요.")




try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
