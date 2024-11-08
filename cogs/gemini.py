import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1000,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="you don't have to provide additional information to explain your response.",
)

class Gemini(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        print(f"Cog {self.__cog_name__} loaded!")

    @commands.hybrid_command(name='en_topic', description='get an AI generated topic', with_app_command=True)
    async def en_topic(self, ctx: commands.Context):
        await ctx.channel.typing()
        result = await model.generate_content_async('generate a topic starter for english learners')
        await ctx.send(result.text)

    @commands.hybrid_command(name='jp_topic', description='AIがトピックを生成してくれるコマンド', with_app_command=True)
    async def jp_topic(self, ctx: commands.Context):
        await ctx.channel.typing()
        result = await model.generate_content_async('日本語を勉強する人向けの一つのトピックスターターを生成せよ')
        await ctx.send(result.text)


async def setup(bot):
    await bot.add_cog(Gemini(bot))