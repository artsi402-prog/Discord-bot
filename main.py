import discord
from discord.ext import commands
import os
import asyncio

TOKEN = "MTQ2MTEyNDk4OTA0MTM4MTM3Ng.Grbgg4.fPW1kfFuNg674tl7gPJTi2FcLza_UkZ5I2MH18"

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ========================
# CHARGEMENT AUTOMATIQUE
# ========================
async def load_extensions():
    for folder in ["cogs", "ai"]:
        if os.path.exists(f"./{folder}"):
            for file in os.listdir(f"./{folder}"):
                if file.endswith(".py"):
                    await bot.load_extension(f"{folder}.{file[:-3]}")
                    print(f"✅ Chargé : {folder}/{file}")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("=================================")
    print(f"🔥 Connecté en tant que {bot.user}")
    print("🔥 100 COMMANDES ACTIVÉES")
    print("=================================")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="100 Commandes Actives 😈"
        )
    )

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())
