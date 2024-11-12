import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from google.cloud import translate_v3

load_dotenv()
gcp_id = os.getenv('GCP_ID')

def translate(
    text: str = '',
    source_code: str = '',
    target_code: str = ''
) -> translate_v3.TranslationServiceClient:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{gcp_id}/locations/global"
    response = client.translate_text(
        contents=[text],
        target_language_code=target_code,
        parent=parent,
        mime_type="text/plain",
        source_language_code=source_code,
    )
    return response.translations[0].translated_text

def detect_language(
        text: str = ''
) -> translate_v3.DetectLanguageResponse:
    client = translate_v3.TranslationServiceClient()
    location = "global"
    parent = f"projects/{gcp_id}/locations/{location}"
    response = client.detect_language(
        content=text,
        parent=parent,
        mime_type="text/plain",
    )
    return response.languages[0].language_code


class Translate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        print(f"Cog {self.__cog_name__} loaded!")

    @commands.hybrid_command(name='translate', description='translate one language to another', with_app_command=True)
    async def translate(self, ctx: commands.Context, *, content):
        await ctx.channel.typing()
        await ctx.defer()
        source_lang = detect_language(text=content)
        if source_lang == 'ja':
            await ctx.reply(translate(text=content, source_code=source_lang, target_code='en-US'), mention_author=False)
        elif source_lang == 'en':
            await ctx.reply(translate(text=content, source_code=source_lang, target_code='ja'), mention_author=False)
        else:
            await ctx.reply('ん？英語か日本語を入力してくださいね～\n\
                            Please submit your arguments in either English or Japanese!')
    
async def setup(bot):
    await bot.add_cog(Translate(bot))