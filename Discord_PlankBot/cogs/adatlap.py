import discord
from discord import Color, Status
from discord.ext import commands
import json

class AdatSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Adatlap System Cog Online')

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def adatlap(self, ctx, user: discord.Member = None):
        users = dbload('users')

        if user == None:
            user = ctx.author

        colour = user.top_role.color

        if colour.value == 0:
            colour = Color.from_rgb(138, 124, 116)

        embed = discord.Embed(title="Adatlap",
                              description="{} adatlapja".format(user.name),
                              color=colour
                              )

        embed.set_author(name=user,
                         url="https://discord.com/users/{}".format(user.id))

        embed.set_thumbnail(url=user.avatar_url)

        embed.set_footer(
            text='Regisztrált: {}\n'
                 'Szerverhez csatlakozott: {}\n'
                 'ID: {}'.format(user.created_at.strftime('%Y.%m.%d %H'), user.joined_at.strftime('%Y.%m.%d %H:%M'), user.id)
        )

        status = user.status

        if status == Status.online:
            embed.add_field(
                name='Állapot',
                value='Online',
                inline=False
            )
        elif status == Status.dnd:
            embed.add_field(
                name='Állapot',
                value='Ne Zavarj!',
                inline=False
            )
        elif status == Status.idle:
            embed.add_field(
                name='Állapot',
                value='Nincs gépnél',
                inline=False
            )
        else:
            embed.add_field(
                name='Állapot',
                value='Offline',
                inline=False
            )

        try:
            # SZINT
            embed.add_field(name="Szint:",
                            value=users[str(ctx.guild.id)][str(user.id)]['lvl'],
                            inline=True)

            # XP
            embed.add_field(name="Tapasztalat:",
                            value=users[str(ctx.guild.id)][str(user.id)]['exp'],
                            inline=True)

        except KeyError:
            embed.add_field(name="Szint:",
                            value='0',
                            inline=True)
            embed.add_field(name="Tapasztalat:",
                            value='0',
                            inline=True)

        try:
            # PLANKPASS TIER
            lvl = dbload('premiumusers')
            if users[str(ctx.guild.id)][str(user.id)]["plankpass"]:

                embed.add_field(name="Tier:",
                                value=lvl[str(ctx.guild.id)][str(user.id)]['lvl'], inline=False)

            else:
                embed.add_field(
                    name='Tier:',
                    value='{}\n'
                          'Ez a felhasználó nem rendelkezik PlankPass-sel.'.format(
                        lvl[str(ctx.guild.id)][str(user.id)]['lvl']),
                    inline=False
                )

        except KeyError:
            embed.add_field(
                name='Tier:',
                value='0\n'
                      'Ez a felhasználó nem rendelkezik PlankPass-sel.',
                inline=False
            )
        finally:
            del lvl


        try:
            # EGYENLEG
            if users[str(ctx.guild.id)][str(user.id)]['bal'] >= 0:
                embed.add_field(name="Egyenleg:",
                                value="{:,} <:plancoin:799180662166781992>".format(
                                    users[str(ctx.guild.id)][str(user.id)]['bal']),
                                inline=False)

            else:
                embed.add_field(name="Tartozás:",
                                value="-{:,} <:plancoin:799180662166781992>".format(
                                    -(users[str(ctx.guild.id)][str(user.id)]['bal'])),
                                inline=False)

        except KeyError:
            embed.add_field(name="Egyenleg:",
                            value="0 <:plancoin:799180662166781992>",
                            inline=False)

        # BOOSTER
        if user.premium_since is not None:
            embed.add_field(
                name='Szerver Booster',
                value='{} óta boostolja a szervert.'.format(user.premium_since.strftime('%Y.%m.%d')),
                inline=False
            )

        # LOTTO TOPLIST
        list = dbload('lottowinners')

        if user.id in list:
            embed.add_field(
                name='Lottó nyertes',
                value='Ez a felhasználó az utolsó 10 lottó nyertes között van.',
                inline=False
            )

        del list

        # UNIVERSAL CARDS
        cards = dbload('globalusers')

        if str(user.id) in cards:
            cards = cards[str(user.id)]
            value = ''
            for i in cards:
                value += '-'
                value += cards[str(i)]['name']
                value += '\n'

            embed.add_field(
                name='Univerzális kártyák',
                value='{}'.format(value),
                inline=False
            )

        # RANGOK
        index = len(user.roles)-1
        roles = ""
        while index > 0:
            roles += user.roles[index].mention + " "
            index -= 1

        if not len(roles) == 0:
            if len(roles) < 800:
                embed.add_field(name="Rangok:",
                                value=roles,
                                inline=False)
            else:
                embed.add_field(
                    name='Rangok:',
                    value='{} rangja van:\n'
                          'Legnagyobb rang: {}'.format(len(user.roles), user.top_role.mention),
                                                  inline=False
                )

        else:
            embed.add_field(name='Nincs rangja',
                            value='---',
                            inline=False)

        await ctx.send(ctx.author.mention, embed=embed)

    @adatlap.error
    async def adatlap_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb adatlap <@tag>`',
                inline=False,
            )

            await ctx.send(embed=embed)

    @adatlap.command(aliases=['állapot', 'status'])
    @commands.guild_only()
    async def allapot(self, ctx, user : discord.Member = None):

        if user == None:
            user = ctx.author

        colour = user.top_role.color

        if colour.value == 0:
            colour = Color.from_rgb(138, 124, 116)

        embed = discord.Embed(title="Adatlap - PlankPass",
                              description="{} adatlapja".format(user.name),
                              color=colour)

        embed.set_footer(
            text='Regisztrált: {}\n'
                 'Szerverhez csatlakozott: {}\n'
                 'ID: {}'.format(user.created_at.strftime('%Y.%m.%d %H'), user.joined_at.strftime('%Y.%m.%d %H:%M'),
                                 user.id)
        )

        embed.set_author(name=user,
                         url="https://discord.com/users/{}".format(user.id))

        embed.set_thumbnail(url=user.avatar_url)

        status = user.status

        if status == Status.online:
            embed.add_field(
                name='Állapot',
                value='Online',
                inline=False
            )
        elif status == Status.dnd:
            embed.add_field(
                name='Állapot',
                value='Ne Zavarj!',
                inline=False
            )
        elif status == Status.idle:
            embed.add_field(
                name='Állapot',
                value='Nincs gépnél',
                inline=False
            )
        else:
            embed.add_field(
                name='Állapot',
                value='Offline',
                inline=False
            )

        await ctx.send(ctx.author.mention, embed=embed)

    @allapot.error
    async def allapot_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb adatlap allapot <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @adatlap.command(aliases=['kártyák'])
    @commands.guild_only()
    async def kartyak(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        colour = user.top_role.color

        if colour.value == 0:
            colour = Color.from_rgb(138, 124, 116)

        embed = discord.Embed(title="Adatlap - kártyák",
                              description="{} adatlapja".format(user.name),
                              color=colour
                              )

        embed.set_author(name=user,
                         url="https://discord.com/users/{}".format(user.id))

        embed.set_thumbnail(url=user.avatar_url)

        embed.set_footer(
            text='Regisztrált: {}\n'
                 'Szerverhez csatlakozott: {}\n'
                 'ID: {}'.format(user.created_at.strftime('%Y.%m.%d %H'), user.joined_at.strftime('%Y.%m.%d %H:%M'), user.id)
        )

        # UNIVERSAL CARDS
        cards = dbload('globalusers')

        if str(user.id) in cards:
            cards = cards[str(user.id)]
            value = ''
            for i in cards:
                value += '-'
                value += cards[str(i)]['name']
                value += '\n'

            embed.add_field(
                name='Univerzális kártyák',
                value='{}'.format(value),
                inline=False
            )
        else:
            embed.add_field(
                name='Univerzálist kártyák',
                value='Ennek a tagnak nincsenek Univerzális kártyái.',
                inline=False
            )

        await ctx.send(ctx.author.mention, embed=embed)

    @kartyak.error
    async def kartya_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb adatlap kartya <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @adatlap.command()
    @commands.guild_only()
    async def szint(self, ctx, user: discord.Member = None):
        try:
            users = dbload('users')

            if user == None:
                user = ctx.author

            colour = user.top_role.color

            if colour.value == 0:
                colour = Color.from_rgb(138, 124, 116)

            embed = discord.Embed(title="Adatlap - szint",
                                  description="{} adatlapja".format(user.name),
                                  color=colour)

            embed.set_author(name=user,
                             url="https://discord.com/users/{}".format(user.id))

            embed.set_thumbnail(url=user.avatar_url)

            embed.set_footer(
                text='Regisztrált: {}\n'
                     'Szerverhez csatlakozott: {}\n'
                     'ID: {}'.format(user.created_at.strftime('%Y.%m.%d %H'), user.joined_at.strftime('%Y.%m.%d %H:%M'),
                                     user.id)
            )

            embed.add_field(name="Szint:",
                            value=users[str(ctx.guild.id)][str(user.id)]['lvl'],
                            inline=True)

            embed.add_field(name="Tapasztalat:",
                            value=users[str(ctx.guild.id)][str(user.id)]['exp'],
                            inline=True)

        except KeyError:
            embed.add_field(name="Szint:",
                            value=0,
                            inline=True)

            embed.add_field(name="Tapasztalat:",
                            value=0,
                            inline=False)

        finally:
            await ctx.send(ctx.author.mention, embed=embed)

    @szint.error
    async def szint_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb adatlap szint <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @adatlap.command(aliases=['boost'])
    @commands.guild_only()
    async def booster(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        if user.premium_since != None:
            embed = discord.Embed(title="Adatlap - Szerver Boost",
                                  description="{} adatlapja".format(user.name),
                                  color=0xFF73FA)
            embed.add_field(
                name='Szerver Booster',
                value='{} óta boostolja a szervert.'.format(user.premium_since.strftime('%Y.%m.%d')),
                inline=False
            )
        else:

            colour = user.top_role.color

            if colour.value == 0:
                colour = Color.from_rgb(138, 124, 116)

            embed = discord.Embed(title="Adatlap - Szerver Boost",
                                  description="{} adatlapja".format(user.name),
                                  color=colour)
            embed.add_field(
                name='Szerver Tag',
                value='Nem boostolja a szervert.',
                inline=False
            )

        embed.set_author(name=user,
                         url="https://discord.com/users/{}".format(user.id))

        embed.set_thumbnail(url=user.avatar_url)

        embed.set_footer(
            text='Regisztrált: {}\n'
                 'Szerverhez csatlakozott: {}\n'
                 'ID: {}'.format(user.created_at.strftime('%Y.%m.%d %H'), user.joined_at.strftime('%Y.%m.%d %H:%M'), user.id)
        )

        await ctx.send(ctx.author.mention, embed=embed)

    @booster.error
    async def booster_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb adatlap booster <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @adatlap.command()
    @commands.guild_only()
    async def plankpass(self, ctx, user: discord.Member = None):
        users = dbload('users')

        try:
            if user == None:
                user = ctx.author

            colour = user.top_role.color

            if colour.value == 0:
                colour = Color.from_rgb(138, 124, 116)

            embed = discord.Embed(title="Adatlap - PlankPass",
                                  description="{} adatlapja".format(user.name),
                                  color=colour)

            embed.set_author(name=user,
                             url="https://discord.com/users/{}".format(user.id))

            embed.set_thumbnail(url=user.avatar_url)

            embed.set_footer(
                text='Regisztrált: {}\n'
                     'Szerverhez csatlakozott: {}\n'
                     'ID: {}'.format(user.created_at.strftime('%Y.%m.%d %H'), user.joined_at.strftime('%Y.%m.%d %H:%M'),
                                     user.id)
            )

            lvl = dbload('premiumusers')
            if users[str(ctx.guild.id)][str(user.id)]["plankpass"]:

                embed.add_field(name="Tier:",
                                value=lvl[str(ctx.guild.id)][str(user.id)]['lvl'], inline=False)

            else:
                embed.add_field(
                    name='Tier:',
                    value='{}\n'
                          'Ez a felhasználó nem rendelkezik PlankPass-sel.'.format(
                        lvl[str(ctx.guild.id)][str(user.id)]['lvl']),
                    inline=False
                )

        except KeyError:
            embed.add_field(
                name='Tier:',
                value='0\n'
                      'Ez a felhasználó nem rendelkezik PlankPass-sel.',
                inline=False
            )
        finally:
            await ctx.send(ctx.author.mention, embed=embed)

    @plankpass.error
    async def plankpass_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb adatlap plankpass <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @adatlap.command()
    @commands.guild_only()
    async def egyenleg(self, ctx, user: discord.Member = None):
        users = dbload('users')

        try:
            if user == None:
                user = ctx.author

            colour = user.top_role.color

            if colour.value == 0:
                colour = Color.from_rgb(138, 124, 116)

            embed = discord.Embed(title="Adatlap - Egyenleg",
                                  description="{} adatlapja".format(user.name),
                                  color=colour)

            embed.set_author(name=user,
                             url="https://discord.com/users/{}".format(user.id))

            embed.set_thumbnail(url=user.avatar_url)

            embed.set_footer(
                text='Regisztrált: {}\n'
                     'Szerverhez csatlakozott: {}\n'
                     'ID: {}'.format(user.created_at.strftime('%Y.%m.%d %H'), user.joined_at.strftime('%Y.%m.%d %H:%M'),
                                     user.id)
            )

            if users[str(ctx.guild.id)][str(user.id)]['bal'] >= 0:
                embed.add_field(name="Egyenleg:",
                                value="{:,} <:plancoin:799180662166781992>".format(
                                    users[str(ctx.guild.id)][str(user.id)]['bal']))

            else:
                embed.add_field(name="Tartozás:",
                                value="-{:,} <:plancoin:799180662166781992>".format(
                                    -(users[str(ctx.guild.id)][str(user.id)]['bal'])))

        except KeyError:
            embed.add_field(name="Egyenleg:",
                            value="0 <:plancoin:799180662166781992>")

        finally:
            await ctx.send(ctx.author.mention, embed=embed)

    @egyenleg.error
    async def egyenleg_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb adatlap egyenleg <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @adatlap.command(aliases=['toplista', 'lottó'])
    @commands.guild_only()
    async def lotto(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        colour = user.top_role.color

        if colour.value == 0:
            colour = Color.from_rgb(138, 124, 116)

        embed = discord.Embed(title="Adatlap - Lottó státusz",
                              description="{} adatlapja".format(user.name),
                              color=colour)

        embed.set_author(name=user,
                         url="https://discord.com/users/{}".format(user.id))

        embed.set_thumbnail(url=user.avatar_url)

        embed.set_footer(
            text='Regisztrált: {}\n'
                 'Szerverhez csatlakozott: {}\n'
                 'ID: {}'.format(user.created_at.strftime('%Y.%m.%d %H'), user.joined_at.strftime('%Y.%m.%d %H:%M'), user.id)
        )

        list = dbload('lottowinners')

        if user.id in list:
            embed.add_field(
                name='Lottó nyertes',
                value='Ez a felhasználó az utolsó 10 lottó nyertes között van.',
                inline=False
            )
        else:
            embed.add_field(
                name='Még nem nyert',
                value='Ez a felhasználó még nem ért el FŐNYEREMÉNY-t lottón.',
                inline=False
            )

        del list

        await ctx.send(ctx.author.mention, embed=embed)

    @lotto.error
    async def lotto_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb adatlap lotto <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @adatlap.command(aliases=['rang'])
    @commands.guild_only()
    async def rangok(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        colour = user.top_role.color

        if colour.value == 0:
            colour = Color.from_rgb(138, 124, 116)

        embed = discord.Embed(title="Adatlap - Rangok",
                              description="{} adatlapja".format(user.name),
                              color=colour)

        embed.set_author(name=user,
                         url="https://discord.com/users/{}".format(user.id))

        embed.set_thumbnail(url=user.avatar_url)

        embed.set_footer(
            text='Regisztrált: {}\n'
                 'Szerverhez csatlakozott: {}\n'
                 'ID: {}'.format(user.created_at.strftime('%Y.%m.%d %H'), user.joined_at.strftime('%Y.%m.%d %H:%M'), user.id)
        )

        index = len(user.roles) - 1
        roles = ""
        while index > 0:
            roles += user.roles[index].mention + " "
            index -= 1
        if not len(roles) == 0:
            if len(roles) < 800:
                embed.add_field(name="Rangok:",
                                value=roles,
                                inline=False)
            else:
                embed.add_field(
                    name='Rangok:',
                    value='{} rangja van:\n'
                          'Legnagyobb rang: {}'.format(len(user.roles), user.top_role.mention),
                    inline=False
                )
        else:
            embed.add_field(name='Nincs rangja',
                            value='---',
                            inline=False)

        await ctx.send(ctx.author.mention, embed=embed)

    @rangok.error
    async def rangok_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb adatlap rangok <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @adatlap.command(aliases=['kép', 'icon'])
    @commands.guild_only()
    async def kep(self, ctx, user : discord.Member = None):

        if user is None:
            user = ctx.author

        colour = user.top_role.color

        if colour.value == 0:
            colour = Color.from_rgb(138, 124, 116)

        embed = discord.Embed(title="Adatlap - Kép",
                              description="{} adatlapja".format(user.name),
                              color=colour)

        embed.set_author(name=user,
                         url="https://discord.com/users/{}".format(user.id))

        embed.set_image(url=user.avatar_url)

        embed.set_footer(
            text='Regisztrált: {}\n'
                 'Szerverhez csatlakozott: {}\n'
                 'ID: {}'.format(user.created_at.strftime('%Y.%m.%d %H'), user.joined_at.strftime('%Y.%m.%d %H:%M'),
                                 user.id)
        )

        await ctx.send(ctx.author.mention, embed=embed)

    @kep.error
    async def kep_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb adatlap kep <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=['avatár'])
    @commands.guild_only()
    async def avatar(self, ctx, user : discord.Member = None):
        if user is None:
            user = ctx.author

        colour = user.top_role.color

        if colour.value == 0:
            colour = Color.from_rgb(138, 124, 116)

        embed = discord.Embed(title="{} képe".format(user.name),
                              color=colour)

        embed.set_author(name=user,
                         url="https://discord.com/users/{}".format(user.id))

        embed.set_image(url=user.avatar_url)


        await ctx.send(ctx.author.mention, embed=embed)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            embed = newErr('Nem létezik ilyen tag.')

            embed.add_field(
                name='Megadott tag név',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb avatar <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)


def newErr(desc: str):
    embed = discord.Embed(title='Hiba', description=desc, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed


def dbload(name: str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)

def dbsave(db, name: str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)

def setup(bot):
    bot.add_cog(AdatSystem(bot))