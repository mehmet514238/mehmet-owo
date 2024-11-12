import discord
from discord.ext import commands
import sqlite3

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kayit(self, ctx):
        discord_id = ctx.author.id
        conn = sqlite3.connect("owo_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,))
        if cursor.fetchone():
            await ctx.send(f"{ctx.author.name}, zaten kayıtlısınız.")
        else:
            cursor.execute("INSERT INTO users (discord_id) VALUES (?)", (discord_id,))
            conn.commit()
            await ctx.send(f"{ctx.author.name}, başarıyla kaydoldunuz!")
        conn.close()

    @commands.command()
    async def kar_zarar(self, ctx):
        discord_id = ctx.author.id
        conn = sqlite3.connect("owo_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT kar_zarar FROM users WHERE discord_id = ?", (discord_id,))
        result = cursor.fetchone()
        if result:
            await ctx.send(f"{ctx.author.name}, toplam kâr-zarar durumun: {result[0]}")
        else:
            await ctx.send("Öncelikle kaydolmanız gerekiyor.")
        conn.close()

async def setup(bot):
    await bot.add_cog(Economy(bot))
