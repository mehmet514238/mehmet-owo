import discord
from discord.ext import commands
import subprocess

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def repo_guncelle(self, ctx):
        await ctx.send("GitHub reposu güncelleniyor...")
        try:
            subprocess.run(["git", "pull", "origin", "main"], check=True)
            await ctx.send("GitHub reposu başarıyla güncellendi.")
        except subprocess.CalledProcessError:
            await ctx.send("GitHub repo güncellenirken bir hata oluştu.")

async def setup(bot):
    await bot.add_cog(Admin(bot))
