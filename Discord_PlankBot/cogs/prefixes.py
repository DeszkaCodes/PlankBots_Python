import discord
from discord.ext import commands
import json
import datetime


class Prefixes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Prefixes Cog Online')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        pfx = dbload('prefixes')

        muted = dbload('mutes')

        pusers = dbload('premiumusers')

        seasons = dbload('seasons')

        shop = dbload('shops')

        users = dbload('users')

        kamat = dbload('kamat')

        del muted[str(guild.id)]
        del pfx[str(guild.id)]
        del pusers[str(guild.id)]
        del seasons[str(guild.id)]
        del shop[str(guild.id)]
        del users[str(guild.id)]
        del kamat[str(guild.id)]

        embed=discord.Embed(
            title='Bot sikeresen eltávolítva - {}'.format(guild.name),
            description='A Bot valamilyen indok miatt el lett távolítva a szerverről.',
            color=0x8a7c74
        )
        embed.set_footer(
            text='Töröltük a szervert az adatbázisból.'
        )
        embed.add_field(
            name='Lehetséges okok:',
            value='-A Botot kibannolták a szerverről.'
                '\n-A Botot kikickelték a szerverről.'
                '\n-A szerver törölve lett.',
            inline=False
        )
        embed.add_field(
            name='Köszönöm, hogy használtad a Botot',
            value='-PlankBot készítője',
            inline=False
        )

        dbsave(pfx, 'prefixes')
        dbsave(muted, 'mutes')
        dbsave(seasons, 'seasons')
        dbsave(shop, 'shops')
        dbsave(users, 'users')
        dbsave(pusers, 'premiumusers')
        dbsave(kamat, 'kamat')

        await guild.owner.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        pfx = dbload('prefixes')

        muted = dbload('mutes')

        pusers = dbload('premiumusers')

        seasons = dbload('seasons')

        shop = dbload('shops')

        kamat = dbload('kamat')

        kamat[str(guild.id)] = {}
        pfx[str(guild.id)] = {}
        pusers[str(guild.id)] = {}
        seasons[str(guild.id)] = {}
        seasons[str(guild.id)]['date'] = ""
        seasons[str(guild.id)]['name'] = ""
        seasons[str(guild.id)]['role'] = ""
        seasons[str(guild.id)]['siderole'] = None
        seasons[str(guild.id)]['price'] = -1
        seasons[str(guild.id)]['isOn'] = False
        seasons[str(guild.id)]['rewards'] = {}
        for i in range(1, 41):
            seasons[str(guild.id)]['rewards'][str(i)] = {}
        shop[str(guild.id)] = {}
        muted[f'{guild.id}'] = {}
        embed = discord.Embed(title='Bot konfigurálása', description='Minden parancs elé használd a !pb kulcsszavat.',color=0x8a7c74)
        embed.set_thumbnail(url=str(self.bot.user.avatar_url)[:-15])
        embed.set_author(name=guild.owner, url="https://discord.com/users/{}".format(guild.owner.id))
        embed.set_footer(
            text='További információkért !pb help <parancs>'
        )
        embed.add_field(
            name='Bolt konfigurálása - `shop`',
            value='`add role <rang> <ár>`'
                '\n`add card \"<név>\" \"<leírás>\" <ár>`'
                '\n`remove role <azonosító>`'
                '\n`remove card <azonosító>`',
            inline=False
        )
        embed.add_field(
            name='Season konfigurálása - `season`',
            value='`datum <dátum>` - forma: ÉV-HÓNAP-NAP - (2025-05-12)'
                '\n`nev \"<név>\"`'
                '\n`rang <rang>`'
                '\n`ar <ár>`'
                '\n`kezd` - Elkezdi a Seasont',
            inline=False
        )
        embed.add_field(
            name='PlankPass Rewardok konfigurálása - `ppreward`',
            value='`add penz <tier> <pénz>`'
                '\n`add rang <tier> <rang>`'
                '\n`add kartya <tier> \"<név>\" \"<leírás>\"`'
                '\n`remove <tier>`',
            inline=False
        )
        embed.add_field(
            name='Szobák konfigurálása - `channel`',
            value='`szint <szoba>`'
                '\n`welcome <szoba>`',
            inline=False
        )
        embed.add_field(
            name='Rangok konfigurálása - `role`',
            value='`nema <rang>`'
                  '\n`bot <rang>`'
                  '\n`auto <rang>`',
        inline=False
        )

        embed.add_field(
            name='Adatbázis javítása',
            value='Ha gyakran jelentkezik \"KeyError\" hiba.'
                  '\n`fixserver`'
        )

        await guild.owner.send(embed=embed)

        dbsave(pfx, 'prefixes')
        dbsave(muted, 'mutes')
        dbsave(pusers, 'premiumusers')
        dbsave(seasons, 'seasons')
        dbsave(shop, 'shops')

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_channels = True)
    async def channel(self, ctx):

        pfx = dbload('prefixes')[str(ctx.guild.id)]

        embed=discord.Embed(title='Beállított szobák listája',
                            description='Az összes éresítő szoba.',
                            color=0x8a7c74)

        embed.set_author(name=ctx.guild.name,
                         url=f'https://discord.com/users={ctx.guild.owner.id}',
                         icon_url=ctx.guild.icon_url)

        isThere = False


        if 'moneyChnl' in pfx:
            chnl = ctx.guild.get_channel(pfx['moneyChnl'])
            embed.add_field(name='Utalások',
                            value=chnl.mention,
                            inline=False)
            isThere = True

        if 'welcomeChnl' in pfx:
            chnl = ctx.guild.get_channel(pfx['welcomeChnl'])
            embed.add_field(name='Üdvözlés',
                            value=chnl.mention,
                            inline=False)
            isThere = True

        if not isThere:
            embed.add_field(name='Nincs beállítva semmilyen szoba.',
                            value='Szoba beállításához használd:'
                            '\n'
                            '\n!pb channel szint <szoba>'
                            '\n!pb channel welcome <szoba>')
            embed.set_footer(
                text='További információkért !pb help <parancs>'
            )

        await ctx.send(ctx.author.mention, embed=embed)

    @channel.command(aliases=['szintek'])
    @commands.guild_only()
    @commands.has_permissions(manage_channels = True)
    async def szint(self, ctx, channel : discord.TextChannel):
        pfx = dbload('prefixes')

        pfx[str(ctx.guild.id)]['lvlChnl'] = channel.id

        dbsave(pfx, 'prefixes')
        del pfx

        embed=discord.Embed(title='Szintlépés értesítő bekapcsolva.',
                            description='Bekapcsoltad a szintlépések értesítését.',
                            color=0x8a7c74)

        embed.set_author(name=ctx.guild.name,
                         url=f'https://discord.com/users/{ctx.guild.owner.id}',
                         icon_url=ctx.guild.icon_url)

        embed.add_field(name='Értesítések küldése a következő szobába történik',
                        value=channel.mention)

        await ctx.send(ctx.author.mention, embed=embed)

    @szint.error
    async def szint_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg szobát.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb channel szint <#szoba>`'
            )

            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.ChannelNotFound):
            embed = newErr('Nem létezik ilyen szoba.')

            embed.add_field(
                name='Megadott szoba',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb channel szint <#szoba>`',
                inline=False
            )

            await ctx.send(embed=embed)

    @channel.command(aliases=['üdvözöl', 'udvozol', 'udvozlo', 'üdvözlő'])
    @commands.guild_only()
    @commands.has_permissions(manage_channels = True)
    async def welcome(self, ctx, channel : discord.TextChannel):
        pfx = dbload('prefixes')

        pfx[str(ctx.guild.id)]['welcomeChnl'] = channel.id

        dbsave(pfx, 'prefixes')
        del pfx

        embed=discord.Embed(title='Szerver köszöntés bekapcsolva.',
                            description='Bekapcsoltad köszöntés. értesítését.',
                            color=0x8a7c74)

        embed.set_author(name=ctx.guild.name,
                         url=f'https://discord.com/users/{ctx.guild.owner.id}',
                         icon_url=ctx.guild.icon_url)

        embed.add_field(name='Értesítések küldése a következő szobába történik',
                        value=channel.mention)


        await ctx.send(ctx.author.mention, embed=embed)

    @welcome.error
    async def welcome_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg szobát.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb channel welcome <#szoba>`'
            )

            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.ChannelNotFound):
            embed = newErr('Nem létezik ilyen szoba.')

            embed.add_field(
                name='Megadott szoba',
                value=error.argument,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb channel welcome <#szoba>`',
                inline=False
            )

            await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx):
        pfx = dbload('prefixes')[str(ctx.guild.id)]

        pfx = dbload('prefixes')[str(ctx.guild.id)]

        embed=discord.Embed(title='Beállított rangok listája',
                            description='Az összes beállított rang.',
                            color=0x8a7c74)

        embed.set_author(name=ctx.guild.name,
                         url=f'https://discord.com/users={ctx.guild.owner.id}',
                         icon_url=ctx.guild.icon_url)

        isThere = False

        if 'mutedRole' in pfx:
            chnl = ctx.guild.get_role(pfx['mutedRole'])
            embed.add_field(name='Némított rang',
                            value=chnl.mention,
                            inline=False)
            isThere = True

        if 'botRole' in pfx:
            chnl = ctx.guild.get_role(pfx['botRole'])
            embed.add_field(name='Bot rang',
                            value=chnl.mention,
                            inline=False)
            isThere = True

        if 'autoRole' in pfx:
            chnl = ctx.guild.get_role(pfx['autoRole'])
            embed.add_field(name='Automatikus rang',
                            value=chnl.mention,
                            inline=False)
            isThere = True

        if not isThere:
            embed.add_field(name='Nincs beállítva semmilyen rang.',
                            value='Rang beállításához használd:'
                            '\n'
                            '\n!pb role nema <rang>'
                            '\n!pb role bot <rang>'
                            '\n!pb role auto <rang>')
            embed.set_footer(
                text='További információkért !pb help <parancs>'
            )

        await ctx.send(ctx.author.mention, embed=embed)

    @role.command(aliases=['muted', 'néma'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def nema(self, ctx, role : discord.Role):
        pfx = dbload('prefixes')

        pfx[str(ctx.guild.id)]['mutedRole'] = role.id

        dbsave(pfx, 'prefixes')
        del pfx

        embed=discord.Embed(title='Némított rang beállítva.',
                            description='Bekapcsoltad a némítás funkciót.',
                            color=0x8a7c74)

        embed.set_author(name=ctx.guild.name,
                         url=f'https://discord.com/users/{ctx.guild.owner.id}',
                         icon_url=ctx.guild.icon_url)

        embed.add_field(name='A némítottak ezt a rangot fogják kapni',
                        value=role.mention)


        await ctx.send(ctx.author.mention, embed=embed)

    @nema.error
    async def nema_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg rangot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb role nema <@tag>`'
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
                value='`!pb role nema <@rang>`',
                inline=False
            )

            await ctx.send(embed=embed)

    @role.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def bot(self, ctx, role: discord.Role):
        pfx = dbload('prefixes')

        pfx[str(ctx.guild.id)]['botRole'] = role.id

        dbsave(pfx, 'prefixes')
        del pfx

        embed = discord.Embed(title='Bot rang beállítva.',
                              description='Bekapcsoltad a botok automatikus rang besorolását.',
                              color=0x8a7c74)

        embed.set_author(name=ctx.guild.name,
                         url=f'https://discord.com/users/{ctx.guild.owner.id}',
                         icon_url=ctx.guild.icon_url)

        embed.add_field(name='Az új botok ezt a rangot fogják kapni',
                        value=role.mention)

        await ctx.send(ctx.author.mention, embed=embed)

    @bot.error
    async def bot_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg rangot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb role bot <@rang>`'
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
                value='`!pb role bot <@rang>`',
                inline=False
            )

            await ctx.send(embed=embed)

    @role.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def auto(self, ctx, role: discord.Role):
        pfx = dbload('prefixes')

        pfx[str(ctx.guild.id)]['autoRole'] = role.id

        dbsave(pfx, 'prefixes')
        del pfx

        embed = discord.Embed(title='Automatikus rang beállítva.',
                              description='Bekapcsoltad a tagok automatikus rang adását.',
                              color=0x8a7c74)

        embed.set_author(name=ctx.guild.name,
                         url=f'https://discord.com/users/{ctx.guild.owner.id}',
                         icon_url=ctx.guild.icon_url)

        embed.add_field(name='Az új tagok ezt a rangot fogják kapni',
                        value=role.mention)

        await ctx.send(ctx.author.mention, embed=embed)

    @auto.error
    async def auto_role(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg rangot')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb role auto <@rang>`'
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
                value='`!pb role bot <@rang>`',
                inline=False
            )

            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 604800, commands.BucketType.guild)
    async def fixserver(self, ctx):

        #VARIABLES

        server = ctx.guild
        id = str(ctx.guild.id)

        errors = 0
        missing = ''

        #EMBED CREATE

        embed = discord.Embed(
            title='Szerver tesztelése',
            color=0x8a7c74
        )

        embed.set_author(
            name=server.name,
            icon_url=server.icon_url
        )

        embed.set_footer(
            text='Teszt időpontja: {}'.format(datetime.datetime.now().strftime('%Y.%m.%d %H:%M'))
        )

        #MUTES
        mutes = dbload('mutes')

        if id not in mutes:
            mutes[id] = {}
            dbsave(mutes, 'mutes')
            errors += 1
            missing += 'Mutes Database\n'

        del mutes

        #PREFIXES

        pfx = dbload('prefixes')

        if id not in pfx:
            pfx[id] = {}
            dbsave(pfx, 'prefixes')
            errors += 1
            missing += 'Prefixes Database\n'

        del pfx

        #PUSERS

        pusers = dbload('premiumusers')

        if id not in pusers:
            pusers[id] = {}
            dbsave(pusers, 'premiumusers')
            errors += 1
            missing += 'PlankPass Database\n'

        del pusers

        #SEASONS

        seasons = dbload('seasons')

        if id not in seasons:
            seasons[id] = {}
            seasons[id]['date'] = ""
            seasons[id]['name'] = ""
            seasons[id]['role'] = ""
            seasons[id]['siderole'] = None
            seasons[id]['price'] = -1
            seasons[id]['isOn'] = False
            seasons[id]['rewards'] = {}
            for i in range(1, 41):
                seasons[id]['rewards'][str(i)] = {}
            dbsave(seasons, 'seasons')
            errors += 1
            missing += 'Season Database\n'

        del seasons

        #SHOPS

        shops = dbload('shops')

        if id not in shops:
            shops[id] = {}
            dbsave(shops, 'shops')
            errors += 1
            missing += 'Shop Database\n'

        del shops

        #USERS

        users = dbload('users')

        if id not in users:
            users[id] = {}
            dbsave(users, 'users')
            errors += 1
            missing += 'User Database\n'

        del users

        #KAMAT

        kamat = dbload('kamat')

        if id not in kamat:
            kamat[id] = {}
            dbsave(kamat, 'kamat')
            errors += 1
            missing += 'Interest Database\n'

        #EMBED FIELDS

        if errors == 0:
            embed.add_field(
                name='Nincs hiba',
                value='Nem találtunk hibát az adatbázisban.'
            )
        else:
            embed.add_field(
                name='{} hibát találtunk'.format(errors),
                value='Javítva:\n{}'.format(missing)
            )

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
    bot.add_cog(Prefixes(bot))
