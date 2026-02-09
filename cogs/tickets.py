import discord
from discord.ext import commands
from discord import app_commands

STAFF_ROLE_ID = 1464265031955779678  # ⚠️ Mets ton ID rôle staff ici


# =========================
# VIEW PRINCIPALE (PANEL)
# =========================
class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎟️ Créer un ticket", style=discord.ButtonStyle.primary, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        staff_role = guild.get_role(STAFF_ROLE_ID)

        # Vérifie si déjà un ticket
        for channel in guild.text_channels:
            if channel.name == f"ticket-{interaction.user.id}":
                return await interaction.response.send_message(
                    "❌ Tu as déjà un ticket ouvert.",
                    ephemeral=True
                )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.id}",
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="🎫 Ticket Ouvert",
            description=f"{interaction.user.mention} merci de décrire ton problème.\nUn staff va te répondre.",
            color=discord.Color.green()
        )

        await channel.send(embed=embed, view=TicketActions())

        await interaction.response.send_message(
            f"✅ Ticket créé : {channel.mention}",
            ephemeral=True
        )


# =========================
# ACTIONS DANS LE TICKET
# =========================
class TicketActions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Fermer", style=discord.ButtonStyle.secondary, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Ce n'est pas un ticket.", ephemeral=True)

        await interaction.channel.edit(name=f"ferme-{interaction.channel.name}")

        await interaction.response.send_message("🔒 Ticket fermé.")

    @discord.ui.button(label="🗑 Supprimer", style=discord.ButtonStyle.danger, custom_id="delete_ticket")
    async def delete_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not interaction.channel.name.startswith(("ticket-", "ferme-")):
            return await interaction.response.send_message("❌ Ce n'est pas un ticket.", ephemeral=True)

        await interaction.response.send_message("🗑 Suppression du ticket...")
        await interaction.channel.delete()

    @discord.ui.button(label="👮 Mode Staff", style=discord.ButtonStyle.success, custom_id="staff_mode")
    async def staff_mode(self, interaction: discord.Interaction, button: discord.ui.Button):

        staff_role = interaction.guild.get_role(STAFF_ROLE_ID)

        if staff_role not in interaction.user.roles:
            return await interaction.response.send_message("❌ Réservé au staff.", ephemeral=True)

        await interaction.channel.send("👮 Mode staff activé.")


# =========================
# COG
# =========================
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket-panel", description="Envoyer le panel ticket")
    async def ticket_panel(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🎟️ Support",
            description="Clique sur le bouton pour ouvrir un ticket.",
            color=discord.Color.blue()
        )

        await interaction.response.send_message(
            embed=embed,
            view=TicketPanel()
        )


async def setup(bot):
    await bot.add_cog(Tickets(bot))
