import traceback
import discord
from discord.ext import commands
from scripts.helperlib import RandomInt, EmbedSettings, UnexpectedErrorEmbed
from scripts.dbhelper import LocalData
from data.database import db

class Localexp(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        print("Local Experience System Ready")


    # Formula to calculate the LVL without storing it
    def LevelFormula(self, exp : int) -> int:
        return int((exp // 42) ** 0.55)


    # Decides if the user has to be added to the database or already in it
    async def processExp(self, message):
        data = await LocalData.GetData(message.author)

        exp = data.exp
        
        await self.addExp(message, exp)


    # Gets a random number to add to the exp then applies it
    async def addExp(self, message : discord.Message, currentExp):
        exp = currentExp + RandomInt(10, 6)

        db.execute("UPDATE LocalData SET EXP = ? WHERE ServerID = ? AND ID = ?", exp, message.guild.id, message.author.id)
        db.commit()

        currentLvl = self.LevelFormula(currentExp)
        newLvl = self.LevelFormula(exp)

        if newLvl > currentLvl:

            channelId : int = db.record("SELECT LVLChannel FROM ServerData WHERE ID = ?", message.guild.id)

            if channelId:
                channel : discord.TextChannel = message.guild.get_channel(int(channelId[0]))
                if channel:

                    embed=discord.Embed(title="Gratulálunk szintet léptél!", description=f"{message.author.name} új szintre lépett.")
                    embed.set_author(name=message.guild.name, icon_url=message.guild.icon.url)
                    embed.add_field(name="Előző szint", value=currentLvl, inline=True)
                    embed.add_field(name="Új szint", value=newLvl, inline=True)

                    await channel.send(content=message.author.mention, embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        
        print(message.content)
        print(message.is_system())
        print(message.author)
        
        if not message.author.bot or not message.is_system():
            await self.processExp(message)
        

    @commands.command(aliases=["dobogó", "dobogo", "szintek"])
    @commands.guild_only()
    async def toplista(self, ctx : commands.Context):
        toplist = db.records("SELECT ID,EXP FROM LocalData ORDER BY EXP DESC LIMIT 10")


        embed=discord.Embed(title=f"{ctx.guild.name} ranglistája", description="Az tíz legnagyobb szintű tag listája.", color=EmbedSettings.defaultColor())
        embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
        
        if toplist:
            index = 1
            for member in toplist:
                embed.add_field(
                        name=f"{index}. - {ctx.guild.get_member(int(member[0])).display_name}",
                        value=f"{member[1]:,} XP - {self.LevelFormula(member[1])} LVL",
                        inline=False
                    )
        else:
            embed.add_field(name="Nincs még szint a szerveren.", value="Ezen a szerveren eddig még senki nem ért el egy szintet se.")

        await ctx.send(content=ctx.author.mention, embed=embed)


    @toplista.error
    async def toplista_error(self, ctx : commands.Context, error):
        await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())

def setup(bot):
    bot.add_cog(Localexp(bot))
