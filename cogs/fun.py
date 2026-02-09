import discord
from discord.ext import commands
from discord import app_commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="coinflip", description="Pile ou face")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Pile", "Face"])
        await interaction.response.send_message(f"🪙 Résultat : **{result}**")

    @app_commands.command(name="8ball", description="Pose une question")
    async def eightball(self, interaction: discord.Interaction, question: str):
        responses = ["Oui", "Non", "Peut-être", "Jamais", "Certainement"]
        await interaction.response.send_message(
            f"🎱 Question: {question}\nRéponse: {random.choice(responses)}"
        )

    @app_commands.command(name="roll", description="Lancer un dé")
    async def roll(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🎲 Tu as fait : {random.randint(1,6)}")

    @app_commands.command(name="iq", description="Teste ton IQ")
    async def iq(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"🧠 IQ de {interaction.user.mention} : {random.randint(50,150)}"
        )

async def setup(bot):
    await bot.add_cog(Fun(bot))
