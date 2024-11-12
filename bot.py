import discord
from discord.ext import commands
import sqlite3
import os
from dotenv import load_dotenv
import requests
import time

# .env dosyasındaki bot token'ını yükleyin
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("CAPTCHA_API_KEY")

# Veritabanı bağlantısını başlatın
conn = sqlite3.connect("owo_data.db")
cursor = conn.cursor()

# Veritabanında 'users' tablosu oluşturun (eğer yoksa)
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    discord_id INTEGER PRIMARY KEY,
    kar_zarar INTEGER DEFAULT 0,
    message_count INTEGER DEFAULT 0,
    pray_status INTEGER DEFAULT 0,
    random_status INTEGER DEFAULT 0,
    captcha_status INTEGER DEFAULT 0,
    captcha_limit INTEGER DEFAULT 10
)''')
conn.commit()

# Bot için gerekli ayarlar
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# CAPTCHA çözümü için yardımcı fonksiyonlar
def solve_captcha(captcha_site_key, page_url):
    url = 'http://2captcha.com/in.php'
    params = {
        'key': API_KEY,
        'method': 'userrecaptcha',
        'googlekey': captcha_site_key,
        'pageurl': page_url,
        'json': 1
    }
    
    response = requests.post(url, data=params)
    result = response.json()
    
    if result['status'] == 1:
        return result['request']
    else:
        return None

def get_captcha_solution(captcha_id):
    url = f'http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1'
    
    while True:
        response = requests.get(url)
        result = response.json()
        
        if result['status'] == 1:
            return result['request']
        time.sleep(5)

# Bot olayları
@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı.')

@bot.command()
async def kayit(ctx):
    discord_id = ctx.author.id
    cursor.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,))
    if cursor.fetchone():
        await ctx.send(f"{ctx.author.name}, zaten kayıtlısınız.")
    else:
        cursor.execute("INSERT INTO users (discord_id) VALUES (?)", (discord_id,))
        conn.commit()
        await ctx.send(f"{ctx.author.name}, başarıyla kaydoldunuz!")

@bot.command()
async def kar_zarar(ctx):
    discord_id = ctx.author.id
    cursor.execute("SELECT kar_zarar FROM users WHERE discord_id = ?", (discord_id,))
    result = cursor.fetchone()
    if result:
        await ctx.send(f"{ctx.author.name}, toplam kâr-zarar durumun: {result[0]}")
    else:
        await ctx.send("Öncelikle kaydolmanız gerekiyor.")

@bot.command()
async def captcha_doğrula(ctx):
    discord_id = ctx.author.id
    cursor.execute("SELECT captcha_status FROM users WHERE discord_id = ?", (discord_id,))
    result = cursor.fetchone()
    
    if result and result[0] == 1:  # CAPTCHA doğrulama aktifse
        captcha_site_key = 'your_google_recaptcha_site_key'
        page_url = 'https://yourcaptchaurl.com'  # CAPTCHA'nın bulunduğu URL
        
        captcha_id = solve_captcha(captcha_site_key, page_url)
        
        if captcha_id:
            solution = get_captcha_solution(captcha_id)
            if solution:
                cursor.execute("UPDATE users SET captcha_status = 1 WHERE discord_id = ?", (discord_id,))
                conn.commit()
                await ctx.send(f"{ctx.author.name} başarıyla doğrulandı!")
            else:
                await ctx.send(f"{ctx.author.name}, CAPTCHA doğrulaması başarısız.")
        else:
            await ctx.send(f"{ctx.author.name}, CAPTCHA çözümü alınamadı.")
    else:
        await ctx.send(f"{ctx.author.name}, CAPTCHA koruması aktif değil veya doğrulama yapılmamış.")

# Bot'u çalıştır
bot.run(TOKEN)
