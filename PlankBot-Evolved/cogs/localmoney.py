import discord, traceback
from discord.embeds import Embed
from discord.ext import commands
from scripts.dbhelper import LocalData
from data.database import db
from scripts.errorlib import BotUserMentioned, NotEnoughMoney, NegativeParameter
from scripts.helperlib import ErrorEmbed, UnexpectedErrorEmbed, EmbedSettings, TimeInSeconds, RandomInt


class Localmoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Local Money System Ready")


    async def setMoney(self, user : discord.Member, balance : int):
        db.execute(
                "UPDATE LocalData SET BALANCE = ? WHERE ServerID = ? AND ID = ?", 
                balance,
                user.guild.id,
                user.id
            )
        
        db.commit()

    async def addMoney(self, user : discord.Member, amount : int):
        db.execute(
                "UPDATE LocalData SET BALANCE = BALANCE + ? WHERE ServerID = ? AND ID = ?", 
                amount,
                user.guild.id,
                user.id
            )
        
        db.commit()

    async def takeMoney(self, user: discord.Member, amount : int):
        await self.addMoney(user, -amount)

    @commands.command(aliases=["bank", "számla", "pénz"])
    @commands.guild_only()
    async def egyenleg(self, ctx : commands.Context, user : discord.Member = None):

        if not user:
            user = ctx.author
        elif user.bot:
            raise BotUserMentioned(user)

        data : LocalData= await LocalData.GetData(user)

        embed=discord.Embed(title=f"{user.name} egyenlege", description=f"{user.mention} bankszámlájának az egyenlege.", color=EmbedSettings.moneyColor())
        embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
        embed.add_field(name="Egyenleg", value=f"{data.balance:,} PlanCoin", inline=False)

        await ctx.send(content=ctx.author.mention, embed=embed)

    @egyenleg.error
    async def egyenleg_error(self, ctx : commands.Context, error):
        await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())


    @commands.command(aliases=["utalás", "utal"])
    @commands.guild_only()
    async def utalas(self, ctx : commands.Context, reciever : discord.Member, amount : int):
        if reciever.bot:
            raise BotUserMentioned(reciever)

        authorBalance : LocalData = await LocalData.GetData(ctx.author)
        recieverBalance : LocalData = await LocalData.GetData(reciever)

        if amount <= 0:
            raise NegativeParameter()

        if authorBalance.balance-amount >= 0:
            await self.takeMoney(ctx.author, amount)
            await self.addMoney(reciever, amount)

        else:
            raise NotEnoughMoney()

        embed=discord.Embed(title="PlanCoin utalás", description=f"{amount:,} mennyiségű PlanCoin sikeresen átutalva.", color=EmbedSettings.moneyColor())
        embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
        embed.add_field(name="Új egyenleged", value=f"{authorBalance.balance - amount:,} PlanCoin", inline=True)
        embed.add_field(name="Fogadó új egyenlege", value=f"{recieverBalance.balance + amount:,} PlanCoin", inline=True)
        await ctx.send(content=ctx.author.mention, embed=embed)
        
    @utalas.error
    async def utalas_error(self, ctx : commands.Context, error):
        if isinstance(error, NotEnoughMoney):
            embed = ErrorEmbed("")
            embed=discord.Embed(title="PlanCoin utalás", description="Az utalás sikertelen.", color=EmbedSettings.errorColor())
            embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
            embed.add_field(name="Indok", value="Nincs elegendő mennyiség a számládon", inline=True)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed("Nem létezik ilyen tag a szerveren.")
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif(isinstance(error, commands.MissingRequiredArgument)):
            embed = ErrorEmbed("")
            embed.description = f"A(z) '{error.param}' paraméter nincs megadva."
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif(isinstance(error, NegativeParameter)):
            embed = ErrorEmbed("")
            embed.description = "Nem utalhatsz nulla vagy annál kevesebb PlanCoin-t."
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif(isinstance(error, commands.BadArgument)):
            embed = ErrorEmbed("")
            embed.description = "A megadott összeg nem egész szám."
            await ctx.send(content=ctx.author.mention, embed=embed)
        else:
            await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())
        
        
    @commands.command()
    @commands.guild_only()
    async def gazdagok(self, ctx : commands.Context):
        toplist = db.records("SELECT ID,BALANCE FROM LocalData ORDER BY BALANCE DESC LIMIT 10")


        embed=discord.Embed(title=f"{ctx.guild.name} leggazdagabbjai", description="Az tíz leggazdagabb tag listája.", color=EmbedSettings.moneyColor())
        embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
        
        if toplist:
            index = 1
            for member in toplist:
                embed.add_field(
                        name=f"{index}. - {ctx.guild.get_member(int(member[0])).display_name}",
                        value=f"{member[1]:,} PlanCoin",
                        inline=False
                    )
        else:
            embed.add_field(name="Nem találtunk tagot.", value="Ezen a szerveren eddig még senki nem rendelkezik PlanCoin-nal.")

        await ctx.send(content=ctx.author.mention, embed=embed)

    @gazdagok.error
    async def gazdagok_error(self, ctx : commands.Context, error):
        await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())


    @commands.command(aliases=["dolgoz", "munka"])
    @commands.cooldown(1, TimeInSeconds.Minute() * 5, commands.BucketType.member)
    async def work(self, ctx : commands.Context):
        balance : LocalData = await LocalData.GetData(ctx.author)
        
        earned : int = RandomInt(5000,2500)
        
        await self.addMoney(ctx.author, earned)
        
    
    @work.error
    async def work_error(self, ctx : commands.Context, error):
        await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())


def setup(bot):
    bot.add_cog(Localmoney(bot))
