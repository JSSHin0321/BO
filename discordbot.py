import discord
from dotenv import load_dotenv
import os
from datetime
import datetime, timedelta
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

# 보스 kill 시간 저장 및 출력
def save_kill_time(boss_name, kill_time):
    boss_list[boss_name]['last_kill_time'] = kill_time
    print(f'{boss_name}의 마지막 처치 시간: {kill_time}')

# 보스 출현 예상 시간 계산 및 출력
def print_respawn_time(boss_name):
    regen_time = boss_list[boss_name]['regen_time']
    last_kill_time = boss_list[boss_name]['last_kill_time']
    if last_kill_time is None:
        print(f'{boss_name}은(는) 처치 기록이 없습니다.')
        return
    respawn_time = last_kill_time + timedelta(hours=int(regen_time[0]))
    print(f'{boss_name}의 출현 예상 시간: {respawn_time.strftime("%Y-%m-%d %H:%M:%S")}')

# 보스 리스트 출력 및 정렬
def print_boss_list():
    print('보스 리스트')
    print('----------')
    bosses = sorted(boss_list.values(), key=lambda x: x['last_kill_time'] + timedelta(hours=int(x['regen_time'][0])))
    for boss in bosses:
        respawn_time = None
        if boss['last_kill_time'] is not None:
            respawn_time = boss['last_kill_time'] + timedelta(hours=int(boss['regen_time'][0]))
        print(f"{boss['name']}: 출현 예상 시간 {respawn_time.strftime('%Y-%m-%d %H:%M:%S') if respawn_time else '미정'}")

# 보스 kill 기록 초기화
def reset_kill_time(boss_name):
    boss_list[boss_name]['last_kill_time'] = None
    print(f'{boss_name}의 처치 기록이 초기화되었습니다.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(PREFIX):
        command = message.content[len(PREFIX):

    if command.startswith('보스이름 '):
        boss_name = command.split()[1]
        if boss_name not in boss_list:
            await message.channel.send(f'{boss_name}은(는) 등록되지 않은 보스입니다.')
        else:
            if command.endswith(' 컷'):
                save_kill_time(boss_name, message.created_at.astimezone(pytz.timezone('Asia/Seoul')))
            elif command.endswith(' 시간'):
                print_respawn_time(boss_name)
            elif command == '보스':
                print_boss_list()
            elif command.endswith(' 초기화'):
                reset_kill_time(boss_name)
            else:
                await message.channel.send(f'잘못된 명령어입니다. "{PREFIX}도움말"을 입력해 사용 가능한 명령어를 확인하세요.')

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
