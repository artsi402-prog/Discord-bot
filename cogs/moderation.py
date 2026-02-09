from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Cog fonctionne !")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
