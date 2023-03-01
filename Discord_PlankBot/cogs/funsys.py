import discord
from discord.ext import commands
from random import random


class FunSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun System Cog Online")

    @commands.group(invoke_without_command=True, aliases=['RNJesus'])
    @commands.guild_only()
    async def rnjesus(self, ctx):
        embed = discord.Embed(
            title='Valami történik',
            description='Érzel magadban egy furcsa erőt...',
            color=0x8a7c74
        )

        embed.set_image(
            url='https://imgur.com/58Rc1qB.jpg'
        )

        await ctx.send(ctx.author.mention, embed=embed)

    @rnjesus.command()
    @commands.guild_only()
    async def gyerele(self, ctx):
        embed = discord.Embed(
            title='A Tanító megszólalt...',
            color=0x8a7c74
        )

        embed.set_author(
            name='RNJesus',
            icon_url='https://imgur.com/MT02yog.png'
        )

        embed.set_thumbnail(url='https://imgur.com/mdLk4X2.jpg')

        embed.add_field(
            name='Az RNG veled van ifjú {}.'.format(ctx.author.name),
            value='Ezzel RNJesus el is tűnt...'
        )

        embed.set_image(url='https://imgur.com/0RNc0qL.jpg')

        embed.set_footer(
            text='Hirtelen erőt érzel magadban és bízol az RNG-ben'
        )

        await ctx.send(ctx.author.mention, embed=embed)

    @rnjesus.command()
    @commands.guild_only()
    async def segíts(self, ctx, sos: str):
        embed = discord.Embed(
            title='A Tanító megszólalt...',
            color=0x8a7c74
        )
        embed.set_thumbnail(url='https://imgur.com/mdLk4X2.jpg')

        embed.set_author(
            name='RNJesus',
            icon_url='https://imgur.com/MT02yog.png'
        )

        if random() <= 0.5:
            embed.add_field(
                name='Jó jeleket érzek az RNG-ben.',
                value='Próbáld meg amire fogadnál.'
            )
        else:
            embed.add_field(
                name='Rosszat érzek az RNG-ben.',
                value='Inkább ne tedd ezt.'
            )
        embed.set_footer(
            text='Ezzel RNJesus el is tűnt...'
        )

        await ctx.send(ctx.author.mention, embed=embed)

    @segíts.error
    async def segits_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem tettél fel kérdést.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb rnjesus segíts "igen/nem kérdés"`'
            )

            await ctx.send(embed=embed)

    @commands.command(aliases=['gazdagság'])
    @commands.guild_only()
    async def gazdagsag(self, ctx):
        await ctx.send('https://imgur.com/8DcicbX.gif')

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10 * 60, commands.BucketType.member)
    async def kifoszt(self, ctx, user: discord.Member):

        embed = discord.Embed(
            name='Kezeket fel!',
            description='Kifosztod {}-t'.format(user.mention),
            color=0x8a7c74
        )
        embed.set_author(name=user,
                         url="https://discord.com/users/{}".format(ctx.author.id),
                         icon_url=ctx.author.avatar_url
                         )

        embed.set_image(
            url='https://imgur.com/Zhmdm0y.png'
        )

        embed.set_footer(
            text='Ez csak humor, semmi egyenleg változás nem történt.'
        )

        await ctx.send(ctx.author.mention, embed=embed)

    @kifoszt.error
    async def kifoszt_error(self, ctx,  error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtad meg kit akarsz kifosztani.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kifoszt <@tag>`'
            )

            ctx.command.reset_cooldown(ctx)

            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kifoszt <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)


    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5 * 60, commands.BucketType.member)
    async def lecsap(self, ctx, user: discord.Member):

        embed = discord.Embed(
            name='Puff!',
            description='Behúztál egyet {}-nak/nek.'.format(user.mention),
            color=0x8a7c74
        )
        embed.set_author(name=user,
                         url="https://discord.com/users/{}".format(ctx.author.id),
                         icon_url=ctx.author.avatar_url
                         )

        embed.set_image(
            url='https://imgur.com/7lPdNVs.png'
        )

        embed.set_footer(
            text='Kabbe teso :('
        )

        await ctx.send(ctx.author.mention, embed=embed)

    @lecsap.error
    async def lecsap_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtad meg kit akarsz lecsapni...')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb lecsap <@tag>`'
            )

            ctx.command.reset_cooldown(ctx)

            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb lecsap <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=['cursed'])
    @commands.guild_only()
    async def kereszt(self, ctx):
        embed = discord.Embed(
            title='Távozz tőlem!',
            color=0x8a7c74
        )
        embed.set_image(
            url='https://imgur.com/u3wMgdz.gif'
        )
        embed.set_footer(
            text='De tényleg...'
        )

        await ctx.send(ctx.author.mention, embed=embed)

    @kereszt.error
    async def kereszt_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem mondtad meg ki távozzon.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kereszt <@tag>`'
            )

            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kereszt <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)


def newErr(reason: str):
    embed = discord.Embed(title='Hiba', description=reason, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed


def setup(bot):
    bot.add_cog(FunSystem(bot))