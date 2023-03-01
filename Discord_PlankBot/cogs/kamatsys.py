import discord
from discord.ext import commands, tasks
from datetime import datetime
import json
from termcolor import colored

class KamatSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_db.start()
        print('Kamat System Cog Online')

    @tasks.loop(hours=24)
    async def check_db(self):
        kamat = dbload('kamat')

        print(colored('\nUpdate time:{}'.format(datetime.now()), 'green'))

        try:

            for server in kamat:
                for user in kamat[server]:
                    kamat[server][user] += int(kamat[server][user] * 0.025)

            print(colored("Kamat Database Updated", 'green'))

        except Exception as e:

            print(colored("Kamat Database couldn\'t be updated:\n\t{}".format(e), 'yellow'))

        dbsave(kamat, 'kamat')

    @commands.group(invoke_without_command = True)
    @commands.guild_only()
    async def kamat(self, ctx):

        user = ctx.author

        try:
            kamat = dbload('kamat')[str(ctx.guild.id)]

            embed = discord.Embed(
                title='Kamat rendszer',
                description='A kamat számlád',
                color=0xC99B00
            )
            embed.set_author(name=user,
                             url="https://discord.com/users/{}".format(user.id))

            embed.set_thumbnail(url=user.avatar_url)

            if str(user.id) in kamat:
                embed.add_field(
                    name='Számlád egyenlege',
                    value='{:,} <:plancoin:799180662166781992>'.format(kamat[str(user.id)])
                )
            else:
                embed.add_field(
                    name='Nem nyitottál még számlát.',
                    value='Számla nyitáshoz írd be:\n`!pb kamat nyit`'
                )

        except KeyError:
            embed = newErr('Ez a szerver nem szerepel a kamat adatbázisban.')
            embed.add_field(
                name='Jelezd a szerver rendszergazdájának/tulajának.',
                value='** **'
            )

        finally:
            await ctx.send(user.mention, embed=embed)

    @kamat.command()
    @commands.guild_only()
    async def nyit(self, ctx, dep : int = 100000):

        user = ctx.author

        kamat = dbload('kamat')

        bal = balance(self, user, ctx.guild.id)

        if str(user.id) not in kamat[str(ctx.guild.id)]:
            if dep >= 100000:
                if bal >= dep:

                    moneyChange(self, user, ctx.guild.id, -dep)


                    kamat[str(ctx.guild.id)][user.id] = dep

                    dbsave(kamat, 'kamat')

                    # <:plancoin:799180662166781992>
                    # color=0xC99B00

                    embed = discord.Embed(
                        title='Számla megnyitva',
                        description='Sikeresen megnyitottad a számládat.',
                        color=0xC99B00
                    )
                    embed.set_author(name=user,
                                     url="https://discord.com/users/{}".format(user.id))

                    embed.set_thumbnail(url=user.avatar_url)

                    embed.add_field(
                        name='Számlád új egyenlege',
                        value='{:,} <:plancoin:799180662166781992>'.format(dep)
                    )
                    embed.add_field(
                        name='Tranzakció időpontja',
                        value=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    embed.add_field(
                        name='Egyenleged',
                        value='{:,} <:plancoin:799180662166781992>'.format(bal - dep),
                        inline=False
                    )

                else:
                    embed = newErr('Nincs ennyi <:plancoin:799180662166781992> a számládon.')
            else:
                embed = newErr('A számla nyitáshoz, legalább 100,000 <:plancoin:799180662166781992>-t be kell rakni.')
        else:
            embed = newErr('Neked már van nyitott számlád.')

        await ctx.send(user.mention, embed=embed)

    @kamat.command()
    @commands.guild_only()
    async def berak(self, ctx, amount : int):

        user = ctx.author
        kamat = dbload('kamat')

        bal = balance(self, user, str(ctx.guild.id))

        if str(user.id) in kamat[str(ctx.guild.id)]:
            if bal >= amount and amount > 0:

                # <:plancoin:799180662166781992>
                # color=0xC99B00

                moneyChange(self, user, ctx.guild.id, -amount)

                kamat[str(ctx.guild.id)][str(user.id)] += amount
                dbsave(kamat, 'kamat')

                embed = discord.Embed(
                    title='Összeg átutalva',
                    description='Átutaltál a kamat számládra,',
                    color=0xC99B00
                )

                embed.set_author(name=user,
                                 url="https://discord.com/users/{}".format(user.id))

                embed.set_thumbnail(url=user.avatar_url)

                embed.add_field(
                    name='Átutalt összeg',
                    value='{:,} <:plancoin:799180662166781992>'.format(amount)
                )

                embed.add_field(
                    name='Tranzakció időpontja',
                    value=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

                embed.add_field(
                    name='Bankszámládon maradt összeg',
                    value=bal-amount,
                    inline=False
                )


            else:
                embed = newErr('Nincs ennyi pénz a számládon.')

        else:
            embed = newErr('Nincs nyitott számlád.')
            embed.add_field(
                name='Számla nyításhoz írd',
                value='`!pb számla nyit`'
            )

        await ctx.send(user.mention, embed=embed)

    @berak.error
    async def berak_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtad meg mennyit PlanCoin-t akarsz berakni.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kamat berak <összeg>`'
            )

            await ctx.send(embed=embed)

    @kamat.command()
    @commands.guild_only()
    async def kivesz(self, ctx, amount):
        user = ctx.author
        kamat = dbload('kamat')

        try:
            if str(user.id) in kamat[str(ctx.guild.id)]:
                bal = kamat[str(ctx.guild.id)][str(user.id)]

                if amount == 'all':
                    amount = bal
                else:
                    amount = int(amount)
                if bal >= amount and amount > 0:

                    # <:plancoin:799180662166781992>
                    # color=0xC99B00

                    moneyChange(self, user, ctx.guild.id, amount)
                    kamat[str(ctx.guild.id)][str(user.id)] -= amount
                    dbsave(kamat, 'kamat')

                    embed = discord.Embed(
                        title='Összeg átutalva',
                        description='Átutaltál a bankszámládra,',
                        color=0xC99B00
                    )

                    embed.set_author(name=user,
                                     url="https://discord.com/users/{}".format(user.id))

                    embed.set_thumbnail(url=user.avatar_url)

                    embed.add_field(
                        name='Átutalt összeg',
                        value='{:,} <:plancoin:799180662166781992>'.format(amount)
                    )

                    embed.add_field(
                        name='Tranzakció időpontja',
                        value=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )

                    embed.add_field(
                        name='Kamat számládon maradt összeg',
                        value=bal - amount,
                        inline=False
                    )

                else:
                    embed = newErr('Nincs ennyi pénz a kamat számládon.')

            else:
                embed = newErr('Nincs nyitott számlád.')
                embed.add_field(
                    name='Számla nyításhoz írd',
                    value='`!pb számla nyit`'
                )

        except ValueError:
            embed = newErr('Helytelen paraméterek.')
            embed.add_field(
                name='Helyes parancs:',
                value='`!pb kamat kivesz <all/összeg>`'
            )

        finally:

            await ctx.send(user.mention, embed=embed)

    @kivesz.error
    async def kivesz_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtad meg mennyi PlanCoin-t veszel ki.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kamat kivesz <összeg>`'
            )

            await ctx.send(embed=embed)

def dbload(name : str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)


def dbsave(db, name : str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)


def moneyChange(self, user: discord.User, serverId, amount):
    users = dbload('users')

    users[f'{serverId}'][f'{user.id}']['bal'] += amount

    dbsave(users, 'users')


def newErr(reason: str):
    embed = discord.Embed(title='Hiba', description=reason, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed


def balance(self, user: discord.User, serverId):
    users = dbload('users')
    return users[f'{serverId}'][f'{user.id}']['bal']


def setup(bot):
    bot.add_cog(KamatSystem(bot))