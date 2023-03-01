import discord
from discord.ext import commands
from datetime import datetime
from random import randint
import json


class ShopSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Shop System Cog Online")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def bolt(self, ctx):
        shop = dbload('shops')

        seasons = dbload('seasons')

        server = ctx.guild
        serverId = str(server.id)
        goods = shop[serverId]

        embed = discord.Embed(title="Plank Bolt", description="Üdvözlünk a boltban!")
        embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                         icon_url=ctx.author.avatar_url)

        if seasons[serverId]['isOn']:
            embed.add_field(
                name='------------------------------',
                value='** **',
                inline=False
            )

            embed.add_field(name=
                            '\nPlankPass', value=seasons[serverId]['name'], inline=True)
            embed.add_field(name='Ár:', value='{:,} <:plancoin:799180662166781992>'.format(seasons[serverId]['price']))
            del seasons

        for item in shop[str(serverId)]:

            if goods[item]['isRole']:

                role = ctx.guild.get_role(goods[item]['give'])
                # embed.add_field(name="------------------------------", value=goods[item]['desc'], inline=False)
                embed.add_field(name='------------------------------'
                                     '\nAzonosító', value=goods[item]['id'], inline=False)
                embed.add_field(name="Termék", value=role.mention, inline=True)
                embed.add_field(name="Ár", value='{:,} <:plancoin:799180662166781992>'.format(goods[item]['price']),
                                inline=True)

            else:
                # embed.add_field(name="------------------------------", value=goods[item]['desc'], inline=False)
                embed.add_field(name='------------------------------'
                                     '\nAzonosító', value=goods[item]['id'], inline=False)

                embed.add_field(name="Termék", value=goods[item]['name'], inline=True)

                embed.add_field(name="Leírás", value=goods[item]['desc'], inline=True)

                embed.add_field(name="Ár", value='{:,} <:plancoin:799180662166781992>'.format(goods[item]['price']),
                                inline=False)

        embed.add_field(name='------------------------------'
                             '\nVásárlás parancsa:', value='!pb bolt vesz <azonosító>', inline=False)
        embed.add_field(name='PlankPass vásárlás:', value='!pb bolt plankpass'
                                                          '\nGift: !pb bolt plankpass <név>', inline=False)

        await ctx.send(ctx.author.mention, embed=embed)

    @bolt.command()
    @commands.guild_only()
    async def vesz(self, ctx, id: str):
        try:

            shop = dbload("shops")

            bal = balance(ctx.author, ctx.guild)
            price = shop[str(ctx.guild.id)][id]['price']
            date = datetime.now()

            if bal >= price:

                if shop[str(ctx.guild.id)][str(id)]["isRole"]:

                    role = ctx.guild.get_role(shop[str(ctx.guild.id)][id]['give'])
                    del shop

                    if role not in ctx.author.roles:
                        await ctx.author.add_roles(role)

                        changeMoney(ctx.author, ctx.guild, -(price))

                        embed = discord.Embed(title='Sikeres vásárlás!',
                                              description='Vásárlás időpontja: {}'.format(
                                                  date.strftime("%Y-%m-%d %H:%M:%S")),
                                              color=0x8a7c74)

                        embed.set_author(name=ctx.author,
                                         url=f'https://discord.com/users/{ctx.author.id}',
                                         icon_url=ctx.author.avatar_url)

                        embed.add_field(name='Megvásárolt rang',
                                        value=role.mention,
                                        inline=False)

                        embed.add_field(name='Ár',
                                        value='{:,} <:plancoin:799180662166781992>'.format(price),
                                        inline=False)

                        embed.add_field(name='Eddigi egyenleg',
                                        value='{:,} <:plancoin:799180662166781992>'.format(bal),
                                        inline=True)

                        embed.add_field(name='Új egyenleg',
                                        value='{:,} <:plancoin:799180662166781992>'.format(
                                            balance(ctx.author, ctx.guild)),
                                        inline=True)

                        await ctx.send(ctx.author.mention, embed=embed)

                    else:
                        embed = newErr('Már rendelkezel ezzel a ranggal')
                        await ctx.send(ctx.author.mention, embed=embed)

                else:

                    name = shop[str(ctx.guild.id)][str(id)]['name']
                    desc = shop[str(ctx.guild.id)][str(id)]['desc']

                    del shop

                    user = dbload('users')

                    while True:
                        id = randint(0, 5000)
                        if str(id) not in user[str(ctx.guild.id)][str(ctx.author.id)]['cards']:
                            break

                    user[str(ctx.guild.id)][str(ctx.author.id)]['cards'][id] = {}
                    user[str(ctx.guild.id)][str(ctx.author.id)]['cards'][id]['name'] = name
                    user[str(ctx.guild.id)][str(ctx.author.id)]['cards'][id]['desc'] = desc
                    user[str(ctx.guild.id)][str(ctx.author.id)]['cards'][id]['id'] = id

                    changeMoney(ctx.author, ctx.guild, -(price))

                    embed = discord.Embed(title='Sikeres vásárlás!',
                                          description='Vásárlás időpontja: {}'.format(
                                              date.strftime("%Y-%m-%d %H:%M:%S")),
                                          color=0x8a7c74)

                    embed.set_author(name=ctx.author,
                                     url=f'https://discord.com/users/{ctx.author.id}',
                                     icon_url=ctx.author.avatar_url)

                    embed.add_field(name='Megvásárolt kártya',
                                    value=name,
                                    inline=False)

                    embed.add_field(name='Leírás',
                                    value=desc,
                                    inline=False)

                    embed.add_field(name='Ár',
                                    value='{:,} <:plancoin:799180662166781992>'.format(price),
                                    inline=False)

                    embed.add_field(name='Eddigi egyenleg',
                                    value='{:,} <:plancoin:799180662166781992>'.format(bal),
                                    inline=True)

                    embed.add_field(name='Új egyenleg',
                                    value='{:,} <:plancoin:799180662166781992>'.format(balance(ctx.author, ctx.guild)),
                                    inline=True)

                    dbsave(user, 'users')

                    await ctx.send(ctx.author.mention, embed=embed)

            else:
                embed = newErr('Nincs elég pénzed.')
                await ctx.send(ctx.author.mention, embed=embed)

        except KeyError:
            embed = newErr('Nincs termék ilyen azonosítóval.')
            await ctx.send(ctx.author.mention, embed=embed)

    @vesz.error
    async def vesz_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg azonosítót.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb bolt vesz <azonosító>`'
            )

            await ctx.send(embed=embed)

    @bolt.command()
    @commands.guild_only()
    async def plankpass(self, ctx, user: discord.Member = None):
        seasons = dbload('seasons')
        serverId = str(ctx.guild.id)

        try:
            if serverId in seasons:
                if seasons[serverId]["isOn"]:
                    price = seasons[serverId]['price']

                    if balance(ctx.author, ctx.guild) >= price:

                        if user is None:

                            user = ctx.author

                            if not hasPP(user, ctx.guild):

                                await addPP(self, user, ctx.guild)

                                embed = discord.Embed(title='Sikeres vásárlás!',
                                                      description='Köszönjük!',
                                                      color=0x8a7c74)

                                embed.set_author(name=ctx.author,
                                                 url=f'https://discord.com/users/{ctx.author.id}',
                                                 icon_url=ctx.author.avatar_url)

                                embed.add_field(name='Megvásároltad:',
                                                value="PlankPass",
                                                inline=False)

                                embed.add_field(name='Ár',
                                                value='{:,} <:plancoin:799180662166781992>'.format(price),
                                                inline=False)

                                changeMoney(ctx.author, ctx.guild, -(price))


                            else:

                                embed = newErr('Már megvan neked a PlankPass.')

                        else:

                            if not hasPP(user, ctx.guild):

                                await addPP(self, user, ctx.guild)

                                embed = discord.Embed(title='Sikeres vásárlás!',
                                                      description='Köszönjük!',
                                                      color=0x8a7c74)

                                embed.set_author(name=ctx.author,
                                                 url=f'https://discord.com/users/{ctx.author.id}',
                                                 icon_url=ctx.author.avatar_url)

                                embed.add_field(name='Megvásároltad:',
                                                value="PlankPass",
                                                inline=False)

                                embed.add_field(name='A következő embernek:',
                                                value=user.mention,
                                                inline=False)

                                embed.add_field(name='Ár',
                                                value='{:,} <:plancoin:799180662166781992>'.format(price),
                                                inline=False)

                                changeMoney(ctx.author, ctx.guild, -(price))


                            else:
                                embed = newErr("Ennek a személynek már megvan a PlankPass")


                    else:
                        embed = newErr('Nincs elég pénzed.')

                else:
                    embed = newErr('Nincs aktív PlankPass a szerveren.')


        except KeyError:
            embed = newErr('Ennek a felhasználónak még nem tudod megvenni a PlankPass-t.')

        await ctx.send(ctx.author.mention, embed=embed)

    @plankpass.error
    async def pp_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb bolt plankpass <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def shop(self, ctx):
        embed = discord.Embed(title='Bolt konfigurálása',
                              description="A következő parancsokkal tudod a boltot konfigurálni.",
                              color=0x8a7c74)
        embed.set_thumbnail(url=str(self.bot.user.avatar_url)[:-15])
        embed.set_author(name=ctx.guild.owner, url="https://discord.com/users/{}".format(ctx.guild.owner.id))
        embed.add_field(name='!pb shop create role|card',
                        value='Bővebb információért, írd be a parancsot paraméter nélkül.')
        embed.set_footer(
            text='További információkért !pb help <parancs>'
        )

        await ctx.send(embed=embed)

    @shop.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def create(self, ctx):
        embed = discord.Embed(title='Bolt konfigurálása - Add',
                              description="A következő parancsokkal tudosz termékeket létrehozni.",
                              color=0x8a7c74)
        embed.add_field(name='!pb shop create role', value='Hozzáad a termékekhez egy rangot'
                                                           '\nParaméterek:'
                                                           '\n<rang> - a rang (mention)'
                                                           '\n<ár> - az vásárlás ára'
                        )
        embed.add_field(name='!pb shop create card', value='Hozzáad a termékekhez egy kártyát'
                                                           '\nParaméterek:'
                                                           '\n<név> - a kártya neve'
                                                           '\n<leírás> - a kártya leírása'
                                                           '\n<ár> - az vásárlás ára'
                        )
        embed.add_field(name='Ha a névbe vagy a leírásba szóközt akarsz rakni, \" jelek közé írd.',
                        value='Pl.: \"Teszt név\" \"Teszt leírás\"')
        await ctx.send(embed=embed)

    @create.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, roleR: discord.Role, price: int):
        shop = dbload('shops')

        try:
            embed = discord.Embed(title='Bolt konfigurálása - Sikeres',
                                  description='Sikeresen hozzáadtak a következő árut:',
                                  color=0x8a7c74)
            serverId = str(ctx.guild.id)
            role = roleR.id
            while True:
                id = randint(0, 5000)
                if id not in shop[serverId]:
                    break;
            shop[serverId][id] = {}
            shop[serverId][id]['id'] = int(id)
            shop[serverId][id]['isRole'] = True
            shop[serverId][id]['give'] = role
            shop[serverId][id]['price'] = int(price)
            embed.add_field(name='Azonosító', value=id)
            embed.add_field(name='Rang', value=roleR.mention)
            embed.add_field(name='Ár', value='{:,} <:plancoin:799180662166781992>'.format(int(price)))
        except ValueError:
            embed = newErr('Nem számot adtál meg árnak.')

        await ctx.send(ctx.author.mention, embed=embed)

        dbsave(shop, 'shops')

    @role.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg rangot vagy árat.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb shop create role <@rang> <ár>`'
            )

            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.RoleNotFound):
            embed = newErr('Nem létezik ilyen rang.')

            embed.add_field(
                name='Megadott rang',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb shop create role <@rang> <ár>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @create.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def card(self, ctx, card: str, desc: str, price: int):
        shop = dbload('shops')

        card = card.replace('_', ' ')
        desc = desc.replace('_', ' ')

        try:
            embed = discord.Embed(title='Bolt konfigurálása - Sikeres',
                                  description='Sikeresen hozzáadtak a következő árut:',
                                  color=0x8a7c74)
            serverId = str(ctx.guild.id)
            while True:
                id = randint(0, 5000)
                if id not in shop[serverId]:
                    break;
            shop[serverId][id] = {}
            shop[serverId][id]['id'] = int(id)
            shop[serverId][id]['isRole'] = False
            shop[serverId][id]['name'] = card
            shop[serverId][id]['desc'] = desc
            shop[serverId][id]['price'] = int(price)
            embed.add_field(name='Azonosító', value=id)
            embed.add_field(name='Név', value=card)
            embed.add_field(name='Leírás', value=desc)
            embed.add_field(name='Ár', value='{:,} <:plancoin:799180662166781992>'.format(int(price)))
        except ValueError:
            embed = newErr('Nem számot adtál meg árnak.')

        await ctx.send(ctx.author.mention, embed=embed)

        dbsave(shop, 'shops')

    @card.error
    async def card_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg nevet, leírást vagy árat.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb shop create card "név" "leírás" <ár>`'
            )

            await ctx.send(embed=embed)

    @shop.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx, id: int):
        shop = dbload('shops')

        try:
            id = str(id)
            embed = discord.Embed(title='Bolt konfigurálása - Sikeres',
                                  description='Sikeresen törölted a következő árut:',
                                  color=0x8a7c74)
            serverId = str(ctx.guild.id)
            embed.add_field(name='Azonosító', value=shop[serverId][id]['id'])
            embed.add_field(name='Ár', value='{:,} <:plancoin:799180662166781992>'.format(shop[serverId][id]['price']))

            del shop[serverId][id]

        except KeyError:
            embed = newErr('Nem létezik termék ilyen azonosítóval.')
        except ValueError:
            embed = newErr('Nem számot adtál azonosítónak.')

        await ctx.send(ctx.author.mention, embed=embed)

        dbsave(shop, 'shops')

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg azonosítót.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb shop delete <azonosító>`'
            )

            await ctx.send(embed=embed)


async def addPP(self, user: discord.Member, server: discord.Guild):
    pusers = dbload('premiumusers')
    users = dbload('users')
    season = dbload('seasons')

    role = server.get_role(season[str(server.id)]['role'])

    await user.add_roles(role)

    users[str(server.id)][str(user.id)]['plankpass'] = True

    if season[str(server.id)]['siderole'] is not None:
        try:
            sideRole = role = server.get_role(season[str(server.id)]['siderole'])
            await user.add_roles(sideRole)
        except:
            print("Battlepass mellek rang törölve")

    if str(user.id) in pusers[str(server.id)]:
        tier = pusers[str(server.id)][str(user.id)]['lvl']

        reward = dbload('seasons')[str(server.id)]['rewards']

        for lvl in range(1, tier):
            if not len(reward[str(lvl)]) == 0:
                if reward[str(lvl)]['type'] == 'role':
                    pprole = server.get_role(reward[str(lvl)]["id"])
                    await user.add_roles(pprole)
            elif reward[str(lvl)]['type'] == 'bal':
                users = dbload('users')
                users[str(server.id)][str(user.id)]['bal'] += reward[str(lvl)]['amount']
                dbsave(users, 'users')
            elif reward[str(lvl)]['type'] == "card":
                users = dbload('users')
                id = reward[str(lvl)]['id']
                name = reward[str(lvl)]['name']
                desc = reward[str(lvl)]['desc']
                users[str(server.id)][str(user.id)]['cards'][id] = {}
                users[str(server.id)][str(user.id)]['cards'][id]['name'] = name
                users[str(server.id)][str(user.id)]['cards'][id]['desc'] = desc
                users[str(server.id)][str(user.id)]['cards'][id]['id'] = id
                dbsave(users, 'users')

    else:
        pusers[f'{server.id}'][f'{user.id}'] = {}
        pusers[f'{server.id}'][f'{user.id}']['exp'] = 0
        pusers[f'{server.id}'][f'{user.id}']['lvl'] = 0

    dbsave(pusers, 'premiumusers')
    dbsave(users, 'users')


def hasPP(user: discord.Member, server: discord.Guild):
    users = dbload('users')

    if users[str(server.id)][str(user.id)]['plankpass']:
        return True
    else:
        return False


def balance(user: discord.Member, server: discord.Guild):
    users = dbload('users')

    return users[str(server.id)][str(user.id)]['bal']


def changeMoney(user: discord.Member, server: discord.Guild, amount):
    users = dbload('users')

    users[str(server.id)][str(user.id)]['bal'] += amount

    dbsave(users, 'users')


def dbload(name: str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)


def dbsave(db, name: str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)


def newErr(reason: str):
    embed = discord.Embed(title='Hiba', description=reason, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed


def setup(bot):
    bot.add_cog(ShopSystem(bot))