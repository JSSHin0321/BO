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
    
    if message.content == f'{PREFIX}보스':
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

    if message.content.startswith(f'{PREFIX}'):
        cmd = message.content[len(PREFIX):].split()
        if cmd[0] == '컷':
            boss_name = cmd[1]
            boss = boss_list.get(boss_name)
            if boss is None:
                await message.channel.send(f"보스 이름이 올바르지 않습니다. ('{boss_name}')")
            else:
                if boss['last_kill_time'] is None:
                    await message.channel.send(f"{boss_name} 보스의 최근 킬 시간 기록이 없습니다.")
                else:
                    last_kill_time = datetime.datetime.strptime(boss['last_kill_time'], '%Y-%m-%d %H:%M:%S.%f')
                    current_time = datetime.datetime.now()
                    elapsed_time = current_time - last_kill_time
                    elapsed_time_str = str(elapsed_time).split('.')[0]
                    await message.channel.send(f"{boss_name} 보스의 마지막 킬 시간 기록: {last_kill_time.strftime('%Y-%m-%d %H:%M:%S')}, 경과 시간: {elapsed_time_str}")
        
        elif cmd[0] in boss_list:
            boss_name = cmd[0]
            boss = boss_list[boss_name]
            if len(cmd) == 1:
                await message.channel.send(f"{boss_name} 보스의 최근 킬 시간 기록: {boss['last_kill_time']}")
            else:
                try:
                    kill_time = datetime.datetime.strptime(cmd[1], '%H%M')
                    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
                    kill_time_str = f"{today_str} {cmd[1][0:2]}:{cmd[1][2:]}:00"
                    boss['last_kill_time'] = kill_time_str
                    await message.channel.send(f"{boss_name} 보스의 최근 킬 시간이 {kill_time_str}로 기록되었습니다.")
                except ValueError:
                    await message.channel.send(f"잘못된 형식의 시간입니다. ('{cmd[1]}')")
        
        else:
            await message.channel.send(f"올바르지 않은 명령어입니다. ('{cmd[0]}')")  




try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
