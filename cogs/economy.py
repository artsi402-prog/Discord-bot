import discord
from discord.ext import commands
from discord import app_commands
import random

balances = {}

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_balance(self, user_id):
        return balances.get(user_id, 0)

    def add_balance(self, user_id, amount):
        balances[user_id] = self.get_balance(user_id) + amount

    @app_commands.command(name="balance", description="Voir ton argent")
    async def balance(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"💰 Solde : {self.get_balance(interaction.user.id)}€"
        )

    @app_commands.command(name="daily", description="Récompense quotidienne")
    async def daily(self, interaction: discord.Interaction):
        amount = random.randint(100,500)
        self.add_balance(interaction.user.id, amount)
        await interaction.response.send_message(
            f"🎁 Tu as reçu {amount}€"
        )

async def setup(bot):
    await bot.add_cog(Economy(bot))
