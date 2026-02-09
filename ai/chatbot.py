import discord
from discord.ext import commands
from discord import app_commands

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ai", description="Parler avec l'IA")
    async def ai_chat(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(
            f"🤖 IA: Tu as dit -> {message}"
        )

async def setup(bot):
    await bot.add_cog(AI(bot))
