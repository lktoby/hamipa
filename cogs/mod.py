import os
import sys
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        print(f"Cog {self.__cog_name__} loaded!")

    @commands.command(name='restart', description='restarts the bot')
    @commands.is_owner()
    async def restart(self, ctx: commands.Context):
        await ctx.send('restarting...')
        print(f'{ctx.author} ({ctx.author.id}) is restarting the bot...')
        os.execv(sys.executable, ['python'] + sys.argv)
    
    @commands.command(name='sync', hidden=True)
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        await ctx.send('syncing commands...')
        sync = await ctx.bot.tree.sync()
        await ctx.send(f'all {len(sync)} commands synced!')

async def setup(bot):
    await bot.add_cog(Mod(bot))