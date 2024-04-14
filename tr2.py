import discord
import os
from deepl import Translator as DeeplTranslator

# Deepl API 키
DEEPL_API_KEY = '6eb802fa-ae94-4f9e-8c72-72d2948fed71'

# Deepl Translator 인스턴스 생성
deepl_translator = DeeplTranslator(DEEPL_API_KEY)

# 디스코드 클라이언트 생성
intents = discord.Intents().all()
client = discord.Client(intents=intents)

# 봇이 작동하기 시작할 때 실행되는 이벤트
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="번역할 준비"))
    print(f'{client.user}로 로그인했습니다.')

# 메시지가 전송될 때마다 실행되는 이벤트
@client.event
async def on_message(message):
    # 봇이 메시지를 보낸 경우 무시
    if message.author == client.user:
        return

    # 슬래시 마크가 포함된 메시지인 경우 무시
    if "/" in message.content:
        return
    
    # 이모지, 인스타그램 링크, gif 링크를 포함한 메시지인 경우 무시
    if message.content.startswith(('http://', 'https://')) or message.content.startswith(('<:', '<a:', '<@')):
        return
    
    # 메시지를 보낸 서버의 언어를 가져옴
    guild_locale = message.guild.preferred_locale
    
    # 메시지 번역
    translations = {}
    languages = {'KO': 'KR', 'ES': 'ES', 'EN-US': 'EN'}
    for lang, lang_name in languages.items():
        translated_message = deepl_translator.translate_text(
            message.content, target_lang=lang
        ).text
        translations[lang_name] = translated_message
    
    # 임베드 생성
    embed = discord.Embed(title="The translation bot has come to translate the message!", description="", color=0x87CEEB)
    for lang_name, translated_message in translations.items():
        embed.add_field(name=lang_name, value=translated_message, inline=False)
    
    # 임베드를 디스코드에 보냄
    await message.channel.send(embed=embed)

# 봇을 실행
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
