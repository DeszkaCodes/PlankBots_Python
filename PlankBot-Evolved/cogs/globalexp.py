import discord
from discord.ext import commands
from data.database import db
from scripts.dbhelper import GlobalData
from scripts.helperlib import RandomInt
from scripts.settings import EmbedSettings


class Globalexp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Global Experience System Ready")


    # Formula to calculate the LVL without storing it
    def LevelFormula(self, exp : int) -> int:
        return int((exp // 42) ** 0.55)

    # Decides if the user has to be added to the database or already in it
    async def processExp(self, ctx):
        data = await GlobalData.GetData(ctx.author)

        exp = data.exp

        await self.addExp(ctx, exp)


    # Gets a random number to add to the exp then applies it
    async def addExp(self, ctx, currentExp):
        exp = currentExp + RandomInt(1,5)

        db.execute("UPDATE GlobalData SET EXP = ? WHERE ID = ?", exp, ctx.author.id)
        db.commit()

        currentLvl = self.LevelFormula(currentExp)
        newLvl = self.LevelFormula(exp)

        if newLvl > currentLvl:

            channelId : int = db.record("SELECT LVLChannel FROM ServerData WHERE ID = ?", ctx.guild.id)

            if channelId:
                channel : discord.TextChannel = ctx.guild.get_channel(int(channelId[0]))
                if channel:

                    embed=discord.Embed(title="Gratulálunk globális szintet léptél!", description=f"{ctx.author.name} új globális szintre lépett.")
                    embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
                    embed.add_field(name="Előző szint", value=currentLvl, inline=True)
                    embed.add_field(name="Új szint", value=newLvl, inline=True)

                    await channel.send(content=ctx.author.mention, embed=embed)


    @commands.Cog.listener()
    async def on_command(self, ctx : commands.Context):
        if not ctx.author.bot:
            await self.processExp(ctx)
        

def setup(bot):
    bot.add_cog(Globalexp(bot))
