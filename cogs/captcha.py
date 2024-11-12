import discord
from discord.ext import commands
import sqlite3

class Captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("owo_data.db")
        self.cursor = self.conn.cursor()

    @commands.command()
    async def captchaprotect(self, ctx, *args):
        if len(args) == 1:
            status = 1 if args[0].lower() == "aç" else 0
            self.cursor.execute("UPDATE users SET captcha_status = ? WHERE discord_id = ?", (status, ctx.author.id))
            self.conn.commit()
            await ctx.send(f"{ctx.author.name}, CAPTCHA koruması {'açıldı' if status else 'kapandı'}.")
        elif len(args) == 2 and args[0].lower() == "cf_limit":
            try:
                limit = int(args[1])
                self.cursor.execute("UPDATE users SET captcha_limit = ? WHERE discord_id = ?", (limit, ctx.author.id))
                self.conn.commit()
                await ctx.send(f"{ctx.author.name}, CAPTCHA mesaj limiti {limit} olarak ayarlandı.")
            except ValueError:
                await ctx.send("Lütfen geçerli bir sayı girin.")
        else:
            await ctx.send("Geçersiz komut.")

async def setup(bot):
    await bot.add_cog(Captcha(bot))
