import discord
from discord.ext import commands
from random import randint
import json

class CardSystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Card System Cog Online")

    @commands.group(aliases=['kártyák', 'kartya', 'kártya'], invoke_without_command=True)
    @commands.guild_only()
    async def kartyak(self, ctx, user : discord.Member = None):

        try:
            if user == None:
                user = ctx.author

            users = dbload('users')[str(ctx.guild.id)][str(user.id)]['cards']
            globalusers = dbload('globalusers')
            embed = discord.Embed(title='Kártyák', description='{} különleges kártyái.'.format(user.mention),
                                  color=0x8a7c74)
            embed.set_author(name=user, url=f'https://discord.com/users/{user.id}', icon_url=user.avatar_url)
            hasCard = False

            if str(user.id) in globalusers:
                hasCard = True
                for id in globalusers[str(user.id)]:
                    embed.add_field(
                        name='{} kártya (universal)'.format(globalusers[str(user.id)][id]['name']),
                        value='{}'.format(globalusers[str(user.id)][id]['desc']),
                        inline=False
                    )

            if not len(users) == 0:
                hasCard = True
                for id in users:
                    embed.add_field(name='{} kártya ({})'.format(users[id]['name'], users[id]["id"]),
                                    value='{}'.format(users[id]['desc']), inline=False)

            if not hasCard:
                embed.add_field(name='Nincs semmilyen kártyája.', value='---', inline=False)

        except KeyError:
            embed=newErr('Ennek a felhasználónak még nem tudod megnézni a kártyáit.')

        finally:
            await ctx.send(ctx.author.mention, embed=embed)

    @kartyak.error
    async def kartyak_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kartyak <@tag>`',
                inline=False
            )

        await ctx.send(embed=embed)

    @kartyak.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def remove(self, ctx, user : discord.Member, id : int):

        try:

            users = dbload('users')

            embed=discord.Embed(title='Kártya eltávolítva',
                                description='Eltávolítottál egy kártyát {}-ról/ről'.format(user.mention),
                                color=0x8a7c74)
            embed.set_author(name=ctx.author,
                             url=f'https://discord.com/user/{ctx.author.id}',
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name='Eltávolított kártya:',
                            value=users[str(ctx.guild.id)][str(ctx.author.id)]['cards'][str(id)]['name'])

            del users[str(ctx.guild.id)][str(ctx.author.id)]['cards'][str(id)]

            await ctx.send('{}\n{}'.format(ctx.author.mention,user.mention), embed=embed)


            dbsave(users, 'users')

        except KeyError:
            embed=newErr('Nem létezik kártya ezzel az azonosítóval.')
            await ctx.send(embed=embed)

        except ValueError:
            embed=newErr('Nem számot adtál meg az azonosítónak.')
            await ctx.send(embed=embed)


    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtad meg a tagot, vagy az azonosítót.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kartya remove <@tag> <kártya id>`'
            )
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kartyak remove <@tag> <kártya id>`',
                inline=False
            )

        await ctx.send(embed=embed)

    @kartyak.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def add(self, ctx, user : discord.Member, name : str, desc : str):

        name = name.replace('_', ' ')
        desc = desc.replace('_', ' ')
        users = dbload('users')

        try:

            id = 0

            #================
            while True:
                id = randint(0,5000)
                if str(id) not in users[str(ctx.guild.id)][str(user.id)]['cards']:
                        break
            #================

            embed=discord.Embed(title='Kártya hozzáadva',
                                description='Adtál egy kártyát {}-nak/nek'.format(user.mention),
                                color=0x8a7c74)
            embed.set_author(name=ctx.author,
                             url=f'https://discord.com/user/{ctx.author.id}',
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name='Hozzáadott kártya:',
                            value='Név: {}'
                                '\nLeírás: {}'
                                '\nID: {}'.format(name,desc,id))

            users[str(ctx.guild.id)][str(user.id)]['cards'][str(id)] = {}
            users[str(ctx.guild.id)][str(user.id)]['cards'][str(id)]['name'] = name
            users[str(ctx.guild.id)][str(user.id)]['cards'][str(id)]['desc'] = desc
            users[str(ctx.guild.id)][str(user.id)]['cards'][str(id)]['id'] = id

            await ctx.send('{}\n{}'.format(ctx.author.mention,user.mention), embed=embed)

            dbsave(users, 'users')

        except KeyError:

            embed=newErr('Nem létezik kártya ezzel az azonosítóval.')
            embed.add_field(
                name='Alternatív probléma',
                value='Ez a tag még 1x sem írt üzenetet.'
            )
            await ctx.send(embed=embed)

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg tagot, nevet vagy leírást.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kartya add <@tag> <név> <leírás>`'
            )
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kartyak add <@tag> "név" "leírás"`',
                inline=False
            )

        await ctx.send(embed=embed)

def dbload(name : str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)


def dbsave(db, name : str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)


def newErr(reason : str):
    embed=discord.Embed(title='Hiba', description=reason, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed


def setup(bot):
    bot.add_cog(CardSystem(bot))
