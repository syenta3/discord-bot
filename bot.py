import discord
from discord.ext import commands
import yt_dlp as youtube_dl

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot olarak giriş yapıldı: {bot.user.name}')

@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        vc = await voice_channel.connect()
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            vc.play(discord.FFmpegPCMAudio(url2))
            await ctx.send(f'Şu an oynatılıyor: {info["title"]}')
    else:
        await ctx.send('Lütfen bir ses kanalına bağlanın.')

@bot.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await ctx.send('Ses kanalından ayrıldım.')
    else:
        await ctx.send('Ses kanalında değilim.')

bot.run('MTExNDk1OTI5MjU5MjgzNjY1MA.GkBbEJ.sWEQlm3QJgguzjQ_aa_5eoa5A5pMI7iw86jPYc')
