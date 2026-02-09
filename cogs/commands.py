import discord
from discord.ext import commands
from discord import app_commands
import random
import datetime

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balance = {}

    # ======================
    # 🛡️ MODERATION
    # ======================

    @app_commands.command(name="kick", description="Expulser un membre")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 {member.mention} a été expulsé.")

    @app_commands.command(name="ban", description="Bannir un membre")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 {member.mention} a été banni.")

    @app_commands.command(name="clear", description="Supprimer des messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"🧹 {amount} messages supprimés.", ephemeral=True)

    @app_commands.command(name="slowmode", description="Activer le slowmode")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        await interaction.channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(f"🐢 Slowmode activé : {seconds}s")

    # ======================
    # 🎮 FUN
    # ======================

    @app_commands.command(name="coinflip", description="Pile ou Face")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Pile 🪙", "Face 🪙"])
        await interaction.response.send_message(f"Résultat : **{result}**")

    @app_commands.command(name="8ball", description="Pose une question magique")
    async def eightball(self, interaction: discord.Interaction, question: str):
        responses = [
            "Oui ✅", "Non ❌", "Peut-être 🤔",
            "Certainement 😎", "Jamais 😈",
            "Demande plus tard ⏳"
        ]
        await interaction.response.send_message(random.choice(responses))

    @app_commands.command(name="roll", description="Lancer un dé")
    async def roll(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🎲 Tu as fait : {random.randint(1,6)}")

    @app_commands.command(name="love", description="Calcul amour")
    async def love(self, interaction: discord.Interaction, member: discord.Member):
        percent = random.randint(0,100)
        await interaction.response.send_message(f"💖 Compatibilité : {percent}%")

    # ======================
    # 📊 UTILITAIRE
    # ======================

    @app_commands.command(name="ping", description="Voir le ping du bot")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Ping : {latency}ms")

    @app_commands.command(name="userinfo", description="Infos sur un membre")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(title="Infos membre", color=discord.Color.blue())
        embed.add_field(name="Nom", value=member.name)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Compte créé", value=member.created_at.strftime("%d/%m/%Y"))
        embed.add_field(name="Rejoint le", value=member.joined_at.strftime("%d/%m/%Y"))
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Infos du serveur")
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild
        embed = discord.Embed(title="Infos Serveur", color=discord.Color.green())
        embed.add_field(name="Nom", value=g.name)
        embed.add_field(name="Membres", value=g.member_count)
        embed.add_field(name="Rôles", value=len(g.roles))
        embed.add_field(name="Salons", value=len(g.channels))
        await interaction.response.send_message(embed=embed)

    # ======================
    # 💰 ECONOMIE SIMPLE
    # ======================

    @app_commands.command(name="daily", description="Réclamer argent journalier")
    async def daily(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        self.balance[user_id] = self.balance.get(user_id, 0) + 100
        await interaction.response.send_message("💰 Tu as reçu 100 coins !")

    @app_commands.command(name="balance", description="Voir ton argent")
    async def balance_cmd(self, interaction: discord.Interaction):
        money = self.balance.get(interaction.user.id, 0)
        await interaction.response.send_message(f"💳 Tu as {money} coins.")

    @app_commands.command(name="work", description="Travailler pour gagner de l'argent")
    async def work(self, interaction: discord.Interaction):
        amount = random.randint(20, 80)
        user_id = interaction.user.id
        self.balance[user_id] = self.balance.get(user_id, 0) + amount
        await interaction.response.send_message(f"💼 Tu as gagné {amount} coins !")


async def setup(bot):
    await bot.add_cog(General(bot))
