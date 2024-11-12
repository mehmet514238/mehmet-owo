import discord
from discord.ext import commands
import sqlite3

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("owo_data.db")
        self.cursor = self.conn.cursor()

    @commands.command()
    async def kayit(self, ctx):
        discord_id = ctx.author.id
        self.cursor.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,))
        if self.cursor.fetchone():
            await ctx.send(f"{ctx.author.name}, zaten kayıtlısınız.")
        else:
            self.cursor.execute("INSERT INTO users (discord_id) VALUES (?)", (discord_id,))
            self.conn.commit()
            await ctx.send(f"{ctx.author.name}, başarıyla kaydoldunuz!")

    @commands.command()
    async def kar_zarar(self, ctx):
        discord_id = ctx.author.id
        self.cursor.execute("SELECT kar_zarar FROM users WHERE discord_id = ?", (discord_id,))
        result = self.cursor.fetchone()
        if result:
            await ctx.send(f"{ctx.author.name}, toplam kâr-zarar durumun: {result[0]}")
        else:
            await ctx.send("Öncelikle kaydolmanız gerekiyor.")

async def setup(bot):
    await bot.add_cog(Economy(bot))
