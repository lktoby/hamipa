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

class Translate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        print(f"Cog {self.__cog_name__} loaded!")

    @app_commands.command(name='en_translate', description='translate japanese to english')
    async def en_translate(self, interaction: discord.Interaction, *, content: str):
        await interaction.response.defer()
        await interaction.followup.send(translate(text=content, source_code='ja', target_code='en-US'))

    @app_commands.command(name='jp_translate', description='英語を日本語に翻訳する')
    async def jp_translate(self, interaction: discord.Interaction, *, content: str):
        await interaction.response.defer()
        await interaction.followup.send(translate(text=content, source_code='en-US', target_code='ja'))

async def setup(bot):
    await bot.add_cog(Translate(bot))