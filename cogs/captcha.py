import discord
from discord.ext import commands
import requests
import time
import os
from dotenv import load_dotenv

# .env dosyasındaki API anahtarını yükleyin
load_dotenv()
API_KEY = os.getenv("CAPTCHA_API_KEY")

# 2CAPTCHA çözümleme fonksiyonu
def solve_captcha(site_key, page_url):
    url = "http://2captcha.com/in.php"
    params = {
        "key": API_KEY,
        "method": "userrecaptcha",
        "googlekey": site_key,
        "pageurl": page_url,
        "json": 1,
    }

    # CAPTCHA çözümü için istek gönder
    response = requests.post(url, params=params)
    request_result = response.json()

    if request_result["status"] == 1:
        captcha_id = request_result["request"]
        return captcha_id
    else:
        return None

# 2CAPTCHA sonucu almak için fonksiyon
def get_solution(captcha_id):
    url = f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1"
    
    while True:
        response = requests.get(url)
        result = response.json()
        
        if result["status"] == 1:
            return result["request"]
        elif result["status"] == 0:
            time.sleep(5)  # 5 saniye sonra tekrar dene

# Komutlar ve bot işlemleri
class CaptchaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def captchasolve(self, ctx, site_key: str, page_url: str):
        # CAPTCHA çözümüne başla
        captcha_id = solve_captcha(site_key, page_url)

        if captcha_id:
            # CAPTCHA çözümü alana kadar bekle
            solution = get_solution(captcha_id)
            await ctx.send(f"CAPTCHA çözümü tamamlandı! Sonuç: {solution}")
        else:
            await ctx.send("CAPTCHA çözümü başarısız oldu.")

def setup(bot):
    bot.add_cog(CaptchaCog(bot))
