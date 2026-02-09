import discord
from discord.ext import commands
import asyncio
import os

from config import TOKEN
import database  # Initialise la DB automatiquement

# =========================
# INTENTS
# =========================
intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# =========================
# AUTO LOAD EXTENSIONS
# =========================
async def load_extensions():
    for folder in ["cogs", "ai"]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith(".py"):
                    try:
                        await bot.load_extension(f"{folder}.{file[:-3]}")
                        print(f"✅ Chargé : {folder}/{file}")
                    except Exception as e:
                        print(f"❌ Erreur {folder}/{file} : {e}")

# =========================
# READY EVENT
# =========================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("=================================")
    print(f"🔥 Connecté en tant que {bot.user}")
    print(f"🆔 ID : {bot.user.id}")
    print("💎 BOT COMMERCIAL ACTIF")
    print("=================================")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="UltraBot Premium 💎"
        )
    )

# =========================
# XP SYSTEM AUTO
# =========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    from database import cursor, conn

    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id) VALUES (?)
    """, (message.author.id,))

    cursor.execute("""
        UPDATE users SET xp = xp + 5 WHERE user_id=?
    """, (message.author.id,))

    conn.commit()

    await bot.process_commands(message)

# =========================
# ERREURS GLOBALES
# =========================
@bot.event
async def on_app_command_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(
        f"❌ Erreur : {error}",
        ephemeral=True
    )

# =========================
# LANCEMENT BOT
# =========================
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
