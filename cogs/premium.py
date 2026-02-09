import discord
from discord.ext import commands
from discord import app_commands
from database import cursor, conn
from config import OWNER_ID

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_premium(self, guild_id):
        cursor.execute("SELECT * FROM premium WHERE guild_id = ?", (guild_id,))
        return cursor.fetchone() is not None

    @app_commands.command(name="premium-activate", description="Activer premium")
    async def activate(self, interaction: discord.Interaction):

        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message(
                "❌ Réservé au propriétaire.",
                ephemeral=True
            )

        cursor.execute("INSERT OR IGNORE INTO premium (guild_id) VALUES (?)",
                       (interaction.guild.id,))
        conn.commit()

        await interaction.response.send_message("💎 Premium activé !")

async def setup(bot):
    await bot.add_cog(Premium(bot))
