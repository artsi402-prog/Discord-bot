import discord
from discord.ext import commands
import os

TOKEN = "MTQ2MTEyNDk4OTA0MTM4MTM3Ng.Grbgg4.fPW1kfFuNg674tl7gPJTi2FcLza_UkZ5I2MH18"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def load_extensions():
    for folder in ["cogs", "ai"]:
        for file in os.listdir(f"./{folder}"):
            if file.endswith(".py"):
                await bot.load_extension(f"{folder}.{file[:-3]}")
                print(f"✅ Chargé : {folder}/{file}")


@bot.event
async def on_ready():
    print("━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🤖 Connecté : {bot.user}")
    await bot.tree.sync()
    print("✅ Commandes synchronisées")
    print("━━━━━━━━━━━━━━━━━━━━━━")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


import asyncio
asyncio.run(main())
