import discord
from discord.ext import commands
from dotenv import load_dotenv
from gtts import gTTS
import os
import tempfile

load_dotenv()

TOKEN = os.environ['TOKEN']

# Create bot instance without a command prefix
bot = commands.Bot(command_prefix=None, help_command=None)

# Text-to-speech command
@bot.command(name='speak')
async def speak(ctx, *, text: str):
    tts = gTTS(text=text, lang='en', slow=False)
    
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        tts.save(fp.name)
        fp.seek(0)

        voice_client = ctx.voice_client
        if voice_client is None:
            return await ctx.send("I'm not connected to a voice channel.")

        voice_client.stop()
        source = discord.FFmpegPCMAudio(fp.name)

        try:
            voice_client.play(source)
        except discord.ClientException as e:
            await ctx.send(f"An error occurred: {e}")

        os.remove(fp.name)

# Join voice channel command
@bot.command(name='join')
async def join(ctx):
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)

    await channel.connect()

# Leave voice channel command
@bot.command(name='leave')
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')

try:
    bot.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
