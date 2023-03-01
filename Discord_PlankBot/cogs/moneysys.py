import discord
from discord.ext import commands
import json

class MoneySystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Money System Cog Online')


    @commands.command(aliases = ['bank'])
    @commands.guild_only()
    async def egyenleg(self, ctx):
        users = dbload('users')

        user = ctx.author
        balance = users[f'{ctx.message.guild.id}'][f'{user.id}']['bal']
        embed=discord.Embed(title='Egyenleg', description='Az egyenleged a szerveren', color=0xC99B00)
        if balance < 0:
            embed.set_thumbnail(url='https://imgur.com/Lqltz9R.png')
        elif balance == 0:
            embed.set_thumbnail(url="https://imgur.com/gtHdBB4.png")
        elif balance == 1:
            embed.set_thumbnail(url='https://imgur.com/bs4O8Ji.png')
        elif balance < 100000:
            embed.set_thumbnail(url='https://imgur.com/aFJ5GQB.png')
        else:
            embed.set_thumbnail(url='https://imgur.com/uN0HXur.png')
        embed.add_field(name='Összeg', value='{:,} <:plancoin:799180662166781992>'.format(balance), inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases = ['pay', 'utal'])
    @commands.guild_only()
    async def fizet(self, ctx, userR: discord.User, amount : int):
        users = dbload('users')

        try:
            serverId = ctx.message.guild.id
            userT = ctx.author
            balance = users[f'{serverId}'][f'{userT.id}']['bal']

            pfx = dbload('prefixes')

            del pfx

            if amount > 0:
                if balance >= amount:
                    users[f'{serverId}'][f'{userR.id}']['bal'] += amount
                    users[f'{serverId}'][f'{userT.id}']['bal'] -= amount
                    embed = discord.Embed(title='Utalás',
                                          description='{} - {:,} <:plancoin:799180662166781992> átutalva {} részére.'.format(
                                              userT.mention, amount, userR.mention),
                                          color=0xC99B00)
                    embed.set_thumbnail(url="https://imgur.com/49xCmq3.png")
                    embed.add_field(name='Új egyenleged:', value='{:,} <:plancoin:799180662166781992>'.format(
                        users[f'{serverId}'][f'{userT.id}']['bal']))

                else:
                    embed = newErr(f'{userT.mention} - Nem rendelkezel ennyi pénzzel.')
                    embed.add_field(name='Egyenleged:', value='{:,} <:plancoin:799180662166781992>'.format(balance))
                    embed.add_field(name='Utalni kívánt összeg:',
                                    value='{:,} <:plancoin:799180662166781992>'.format(amount))

            else:
                embed = newErr('Nem utalhatsz 0 vagy kevesebb -t.')

            dbsave(users, 'users')

        except KeyError:
            embed=newErr('Ennek a felhasználónak még nem utalhatsz pénzt.')

        finally:
            await ctx.send(ctx.author.mention, embed=embed)

    @fizet.error
    async def fizet_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            embed=newErr('Rossz értékeket adtál meg.')
            embed.add_field(name='Helyes parancs: ', value='!pb fizet <@név> <pénz>')

        elif isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtad meg a kódot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb code <kód>`'
            )

        elif isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb fizet <@tag> <összeg>`',
                inline=False
            )

        await ctx.send(embed=embed)


    @commands.command(aliases = ['adminFizet', 'adminPay', 'adminpay'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def adminfizet(self, ctx, user : discord.User, amount : int):
        try:
            users = dbload('users')

            users[f'{ctx.message.guild.id}'][f'{user.id}']['bal'] += amount

            embed = discord.Embed(
                title='Pénz elküldve'
            )

            embed.set_author(
                name=ctx.author,
                url=f'https://discord.com/users/{ctx.author.id}',
                icon_url=ctx.author.avatar_url
            )

            embed.add_field(
                name='Összeg',
                value='{:,} <:plancoin:799180662166781992>'.format(amount)
            )

            dbsave(users, 'users')

        except KeyError:
            embed = newErr('Ennek a felhasználónak még nem lehet pénzt adni.')

        finally:
            await ctx.send(ctx.author.mention, embed=embed)

    @adminfizet.error
    async def adminfizet_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg tagot vagy összeget.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb adminfizet <@tag> <összeg>`'
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
                value='`!pb adminfizet <@tag> <összeg>`',
                inline=False
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.BadArgument):
            embed = newErr('Rossz értékeket adtál meg.')
            embed.add_field(name='Helyes parancs: ', value='!pb adminfizet <@név> <pénz>')
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 604800, commands.BucketType.guild)
    async def pcreset(self, ctx):

        try:
            serverId = str(ctx.guild.id)
            users = dbload('users')
            kamat = dbload('kamat')

            del kamat[str(ctx.guild.id)]
            kamat[ctx.guild.id] = {}

            dbsave(kamat, 'kamat')

            for i in users[serverId]:
                users[serverId][i]['bal'] = 0

            dbsave(users, 'users')

            embed = discord.Embed(
                title='Szerver PlanCoin nullázva',
                description='Mindenkinek lenulláztad az egyenlegét a szerveren.',
                color=0xC99B00
            )

            embed.set_author(
                name=ctx.author,
                url="https://discord.com/users/{}".format(ctx.author.id),
                icon_url=ctx.author.avatar_url
            )

            embed.set_thumbnail(
                url='https://imgur.com/Lqltz9R.png'
            )

            embed.set_footer(
                text='A parancs egy hét múlva újra elérhető lesz.'
            )

        except:
            embed = newErr('Egy hiba lépett fel, próbáld újra.')
            ctx.command.reset_cooldown(ctx)

        finally:
            await ctx.send(ctx.author.mention, embed=embed)



def newErr(reason : str):
    embed=discord.Embed(title='Hiba', description=reason, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed

def dbload(name : str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)

def dbsave(db, name : str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)


def setup(bot):
    bot.add_cog(MoneySystem(bot))
