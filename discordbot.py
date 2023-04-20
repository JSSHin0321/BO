from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import datetime
import pytz
import asyncio


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
    },
    '보드레': {
    'name': '보드레',
    'level': 47,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FczdMFw%2FbtsafNEDJqw%2FL4WgURVrhPothZIoGGVzj1%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '이드라칸': {
    'name': '이드라칸',
    'level': 47,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbqYH7o%2FbtsakgL9a0K%2FdQmBOKbxvH59KYSC7oht9k%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '솔그리드': {
    'name': '솔그리드',
    'level': 47,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F13Tqi%2Fbtsaibq6Ip1%2FZtumDQmO9Fpvkiq1wdTtNK%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '악몽': {
    'name': '악몽',
    'level': 47,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FchFtNo%2Fbtsai46hvqC%2FiOrrLs0FiRQPlL6V6oc3B0%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '카를로스': {
    'name': '카를로스',
    'level': 47,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcgEGC0%2FbtsafQ2jL7m%2FGgLnruWauqt7XqiHj3kGpk%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '분쇄자': {
    'name': '분쇄자',
    'level': 44,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FmO2FO%2Fbtsal3S9ReY%2FkZihlvzeiCDdKDwEGR1FVK%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '다비드': {
    'name': '다비드',
    'level': 44,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbmjUmZ%2FbtsakfT1ktr%2FhSqjg4Pz9hKOkg3dYUJ540%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '아르노슈트': {
    'name': '아르노슈트',
    'level': 44,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FchFtNo%2Fbtsai46hvqC%2FiOrrLs0FiRQPlL6V6oc3B0%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '암몬': {
    'name': '암몬',
    'level': 44,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbS6EiX%2FbtsaibxQI5N%2FeL7dfmI4SnKL5hI6rDXurK%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '이올라': {
    'name': '이롤라',
    'level': 41,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F6SxbD%2FbtsamWsRSwt%2FOR1orqutBTBWfZ1U0ZLCKK%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '라크다르': {
    'name': '라크다르',
    'level': 41,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FczdMFw%2FbtsafNEDJqw%2FL4WgURVrhPothZIoGGVzj1%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '호쏜': {
    'name': '호쏜',
    'level': 41,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FtHoMB%2FbtsamWsRSLj%2FHGeT2v5JnEIdmWm2QIbKh0%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    },
    '기드온': {
    'name': '기드온',
    'level': 41,
    'location': 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdK4pXz%2Fbtsai4ZwHpf%2F5Ft7pk4fGwk0IGfzrYxj81%2Fimg.png',
    'regen_time': '3시간',
    'last_kill_time': None
    }
}



@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

async def send_boss_alert(boss):
    kst = pytz.timezone('Asia/Seoul')
    now_kst = datetime.datetime.now(kst)

    if boss['last_kill_time'] is not None:
        last_kill_time = datetime.datetime.strptime(boss['last_kill_time'], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=pytz.utc)
        regen_time = datetime.timedelta(hours=int(boss['regen_time'][0]))
        expected_spawn_time = (last_kill_time + regen_time).astimezone(kst)
        time_diff = (expected_spawn_time - now_kst).total_seconds() / 60.0

        if 9.5 <= time_diff < 10.5:
            expected_spawn_time_str = expected_spawn_time.strftime('%H:%M:%S')
            boss_info = f"{boss['name']} (Lv. {boss['level']}) ==> {expected_spawn_time_str}"

            embed = discord.Embed(title="보스 출현 알림",
                                  description=f"보스가 10분 후에 출현합니다!",
                                  color=0x2ECC71)  # You can change the color to your preference
            embed.set_footer(text="출현 예정 시간: " + expected_spawn_time_str)
            embed.set_image(url=boss['location'])
            channel = client.get_channel(1097888729693167648)  # Replace YOUR_CHANNEL_ID with the actual channel ID
            await channel.send(embed=embed)





async def check_boss_spawn():
    await client.wait_until_ready()
    while not client.is_closed():
        for boss in boss_list.values():
            await send_boss_alert(boss)
        await asyncio.sleep(60)  # 1분 주기로 실행

client.loop.create_task(check_boss_spawn())
    
    
    
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if not message.content.startswith(PREFIX):
        return
    
    parts = message.content.split()
    command = parts[0][len(PREFIX):]

    if command == '명령어':
        await message.channel.send(
        '보스맵1: 보스 맵 1번 이미지 링크를 보여줍니다.',
        '보스맵2: 보스 맵 2번 이미지 링크를 보여줍니다.',
        '보스: 현재 등록된 모든 보스의 스폰 시간 정보를 보여줍니다.',
        '[보스 이름]: 해당 보스의 위치 이미지 링크를 보여줍니다.',
        '[보스 이름] 컷 : 해당 보스의 last kill time을 갱신합니다.',
        '[보스 이름] [4자리 시간]: 해당 보스의 last kill time을 입력한 시간으로 갱신합니다.'
    )
    
    
    if command == "보스맵1":
        await message.channel.send("https://dszw1qtcnsa5e.cloudfront.net/community/20230404/716418d7-2576-43c3-9580-3d2bf2d77e58/45%EB%B3%B4%EC%8A%A4.png?data-size=5332128")
    
    if command == "보스맵2":
        await message.channel.send("https://dszw1qtcnsa5e.cloudfront.net/community/20230404/29c555d6-eb4b-4674-8955-eae7d94b48d1/50%EB%B3%B4%EC%8A%A4.png?data-size=5311083")
    
    if command == '보스':
        boss_info_list = []
        for boss in sorted(boss_list.values(), key=lambda x: x['last_kill_time'] or '9999-99-99 99:99:99'):
            if boss['last_kill_time'] is None:
                expected_spawn_time = ' '
            else:
                last_kill_time = datetime.datetime.strptime(boss['last_kill_time'], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=pytz.utc)
                regen_time = datetime.timedelta(hours=int(boss['regen_time'][0]))
                kst = pytz.timezone('Asia/Seoul')
                expected_spawn_time = (last_kill_time + regen_time).astimezone(kst)
                expected_spawn_time = expected_spawn_time.strftime('%H:%M:%S')

            boss_info = f"{expected_spawn_time} ==> {boss['name']} (Lv. {boss['level']})"
            boss_info_list.append(boss_info)

        boss_info_str = "\n".join(boss_info_list)
        boss_embed = discord.Embed(title="보스 정보", description=boss_info_str, color=0x00FF00)
        await message.channel.send(embed=boss_embed)



    elif command in boss_list:
        boss = boss_list[command]
        if len(parts) == 1:
            location_link = boss_list[command]['location']
            await message.channel.send(location_link)
        if len(parts) == 2 and parts[1] == '컷':
            boss['last_kill_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            await message.channel.send(f"{boss['name']}의 last kill time이 갱신되었습니다.")
        elif parts[1].isdigit() and len(parts[1]) == 4:
            kst = pytz.timezone('Asia/Seoul')
            now_kst = datetime.datetime.now(kst)
            hour = int(parts[1][:2])
            minute = int(parts[1][2:])
            input_time = now_kst.replace(hour=hour, minute=minute, second=0, microsecond=0)
            utc = pytz.utc
            last_kill_time = input_time.astimezone(utc)
            boss['last_kill_time'] = last_kill_time.strftime('%Y-%m-%d %H:%M:%S.%f')
            await message.channel.send(f"{boss['name']}의 last kill time이 갱신되었습니다.")
        elif parts[1] == '초기화':
            boss['last_kill_time'] = None
            await message.channel.send(f"{boss['name']}의 last kill time이 초기화되었습니다.")
    
        # 갱신된 보스 리스트 출력
        boss_info_list = []
        for boss in sorted(boss_list.values(), key=lambda x: x['last_kill_time'] or '9999-99-99 99:99:99'):
            if boss['last_kill_time'] is None:
                expected_spawn_time = ' '
            else:
                last_kill_time = datetime.datetime.strptime(boss['last_kill_time'], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=pytz.utc)
                regen_time = datetime.timedelta(hours=int(boss['regen_time'][0]))
                kst = pytz.timezone('Asia/Seoul')
                expected_spawn_time = (last_kill_time + regen_time).astimezone(kst)
                expected_spawn_time = expected_spawn_time.strftime('%H:%M:%S')

            boss_info = f"{expected_spawn_time} ==> {boss['name']} (Lv. {boss['level']})"
            boss_info_list.append(boss_info)

        boss_info_str = "\n".join(boss_info_list)
        boss_embed = discord.Embed(title="보스 정보", description=boss_info_str, color=0x00FF00)
        await message.channel.send(embed=boss_embed)







try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
