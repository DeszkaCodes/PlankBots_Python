import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from random import randint
import json
from termcolor import colored


class SeasonSystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_db.start()
        print('Season System Cog Online')

    @tasks.loop(hours=24)
    async def check_db(self):
        seasons = dbload('seasons')

        print(colored('\nUpdate time:{}'.format(datetime.now()), 'green'))

        try:
            for server in seasons.copy():
                if seasons[server]["isOn"]:
                    endDate = datetime.strptime(seasons[server]["date"], '%Y-%m-%d %H:%M:%S')
                    if endDate < datetime.now():
                        pusers = dbload('premiumusers')
                        users = dbload('users')

                        for user in pusers[str(server)].copy():
                            del pusers[str(server)][user]

                        for user in users[str(server)]:
                            users[str(server)][user]['plankpass'] = False

                        dbsave(pusers, 'premiumusers')
                        dbsave(users, 'users')
                        del pusers
                        del users

                        del seasons[str(server)]['rewards']
                        seasons[str(server)]['rewards'] = {}
                        for i in range(1, 41):
                            seasons[str(server)]['rewards'][str(i)] = {}

                        seasons[str(server)]["isOn"] = False
                        seasons[str(server)]["name"] = ""
                        seasons[str(server)]["date"] = ""
                        seasons[str(server)]["role"] = ""
                        seasons[id]['siderole'] = None
                        seasons[str(server)]["price"] = -1
            print(colored("Season Database Updated", 'green'))

        except Exception as e:
            print(colored("Season Database couldn\'t be updated:\n\t{}".format(e), 'yellow'))

        dbsave(seasons, 'seasons')

    @commands.Cog.listener()
    async def on_member_join(self, member):

        seasons = dbload('seasons')

        if seasons[str(member.guild.id)]['isOn']:
            del seasons
            if not member.bot:
                pusers = dbload('premiumusers')

                await update_db(self, pusers, member, member.guild.id)

                dbsave(pusers, 'premiumusers')

    @commands.Cog.listener()
    async def on_message(self, message):

        try:
            if str(message.channel.type) != 'private':

                seasons = dbload('seasons')
                if seasons[str(message.guild.id)]['isOn']:
                    del seasons
                    if not message.author.bot:
                        pusers = dbload('premiumusers')
                        await update_db(self, pusers, message.author, message.guild.id)
                        await addExp(self, pusers, message.author, message.guild)

                        dbsave(pusers, 'premiumusers')

        except KeyError:
            print('Season Key Error\nMessage: {}\nAuthor: {}\nServer: {}'.format(message.content, message.author.name, message.guild.name))

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def ppreward(self, ctx):
        rewards = dbload('seasons')[str(ctx.guild.id)]['rewards']

        embed = discord.Embed(title='PlankPass Nyereményei', description='A season nyereményei',
                              color=0x8a7c74)

        embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                         icon_url=ctx.author.avatar_url)

        embed.set_footer(
            text='További információkért !pb help <parancs>'
        )

        for i in rewards:
            if not len(rewards[i]) == 0:
                if rewards[i]['type'] == "role":
                    role = ctx.guild.get_role(rewards[i]['id'])
                    embed.add_field(name='{}. tier'.format(i), value=role.mention, inline=False)
                elif rewards[i]['type'] == "bal":
                    embed.add_field(name='{}. tier'.format(i),
                                    value='{} <:plancoin:799180662166781992>'.format(rewards[i]['amount']),
                                    inline=False)
                else:
                    embed.add_field(name='{}. tier'.format(i),
                                    value='{} kártya\n{}'.format(rewards[i]['name'], rewards[i]['desc']), inline=False)

        await ctx.send(ctx.author.mention, embed=embed)

    @ppreward.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, tier: int):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']
        if not isOn:
            seasons = dbload('seasons')

            del seasons[str(ctx.guild.id)]['rewards'][str(tier)]

            embed = discord.Embed(
                title='Tier törölve',
                description=None,
                color=0x8a7c74
            )

            embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                             icon_url=ctx.author.avatar_url)

            embed.add_field(
                name='Törölted a következő tier rewardot',
                value=tier
            )

            seasons[str(ctx.guild.id)]['rewards'][str(tier)] = {}

            dbsave(seasons, 'seasons')

        else:
            embed = newErr('Aktív Season-t nem tudsz szerkeszteni.')

        await ctx.send(ctx.author.mention, embed=embed)

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg Tier-t.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb ppreward remove <tier>`'
            )

            await ctx.send(embed=embed)

    @ppreward.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx):
        embed = discord.Embed(title='Ajándék hozzáadása',
                              description='PlankPass Tier Ajándék hozzáadása',
                              color=0x8a7c74)

        embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                         icon_url=ctx.author.avatar_url)

        embed.set_author(name=ctx.guild.name,
                         url=f'https://discord.com/user/{ctx.guild.owner.id}',
                         icon_url=ctx.guild.icon_url)
        embed.add_field(name='Kártya hozzáadása',
                        value='ppreward add kartya <tier> \"<név>\" \"<leírás>\"',
                        inline=False)
        embed.add_field(name='Rang hozzáadása',
                        value='ppreward add rang <tier> <rang>',
                        inline=False)
        embed.add_field(name='PlanCoin hozzáadása',
                        value='ppreward add penz <tier> <összeg>',
                        inline=False)
        embed.set_footer(
            text='További információkért !pb help <parancs>'
        )

        await ctx.send(ctx.author.mention, embed=embed)

    @add.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def penz(self, ctx, tier: int, amount: int):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']
        if not isOn:
            rewards = dbload('seasons')

            if len(rewards[str(ctx.guild.id)]['rewards'][str(tier)]) == 0:
                rewards[str(ctx.guild.id)]['rewards'][str(tier)]['type'] = 'bal'
                rewards[str(ctx.guild.id)]['rewards'][str(tier)]['amount'] = amount

                embed = discord.Embed(title='Tier {}'.format(tier),
                                      description='Ajándéka beállítva.',
                                      color=0x8a7c74)

                embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                                 icon_url=ctx.author.avatar_url)

            else:
                embed = newErr('Ezen a tieren már van ajándék.')

            dbsave(rewards, 'seasons')
        else:
            embed = newErr('Aktív Season-t nem tudsz szerkeszteni.')

        await ctx.send(ctx.author.mention, embed=embed)

    @penz.error
    async def penz_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg Tier-t vagy összeget.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb ppreward add penz <tier> <összeg>`'
            )

            await ctx.send(embed=embed)

    @add.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def rang(ctx, tier: int, role: discord.Role):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']
        if not isOn:
            if not role.is_bot_managed():
                rewards = dbload('seasons')

                if len(rewards[str(ctx.guild.id)]['rewards'][str(tier)]) == 0:
                    rewards[str(ctx.guild.id)]['rewards'][str(tier)]['type'] = 'role'
                    rewards[str(ctx.guild.id)]['rewards'][str(tier)]['id'] = role.id

                    embed = discord.Embed(title='Tier {}'.format(tier),
                                          description='Ajándéka beállítva.',
                                          color=0x8a7c74)

                    embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                                     icon_url=ctx.author.avatar_url)

                else:
                    embed = newErr('Ezen a tieren már van ajándék.')

                dbsave(rewards, 'seasons')

            else:
                embed = newErr('Ez a rang Bot exkluzív.')
                embed.add_field(
                    name='Adj meg másik rangot',
                    value='** **'
                )

        else:
            embed = newErr('Aktív Season-t nem tudsz szerkeszteni.')

        await ctx.send(ctx.author.mention, embed=embed)

    @rang.error
    async def rang_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg Tier-t vagy rangot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb ppreward add rang <tier> <@rang>`'
            )

            await ctx.send(embed=embed)

            if isinstance(error, commands.errors.RoleNotFound):
                embed = newErr('Nem létezik ilyen rang.')

                embed.add_field(
                    name='Megadott rang',
                    value=error.argument,
                    inline=False
                )

                embed.add_field(
                    name='Helyes parancs',
                    value='`!pb ppreward add rang <tier> <@rang>`',
                    inline=False
                )
                await ctx.send(embed=embed)

    @add.command(aliases=['kártya', 'card'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def kartya(self, ctx, tier: int, name: str, desc: str):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']
        if not isOn:
            rewards = dbload('seasons')
            name = name.replace('_', ' ')
            desc = desc.replace('_', ' ')

            if len(rewards[str(ctx.guild.id)]['rewards'][str(tier)]) == 0:
                rewards[str(ctx.guild.id)]['rewards'][str(tier)]['type'] = "card"
                id = 0
                while id in rewards[str(ctx.guild.id)]['rewards']:
                    id = randint(6000, 10000)

                rewards[str(ctx.guild.id)]['rewards'][str(tier)]['id'] = id
                rewards[str(ctx.guild.id)]['rewards'][str(tier)]['name'] = name
                rewards[str(ctx.guild.id)]['rewards'][str(tier)]['desc'] = desc

                embed = discord.Embed(title='Tier {}'.format(tier),
                                      description='Ajándéka beállítva.',
                                      color=0x8a7c74)

                embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                                 icon_url=ctx.author.avatar_url)

            else:
                embed = newErr('Ezen a tieren már van ajándék.')

            dbsave(rewards, 'seasons')
        else:
            embed = newErr('Aktív Season-t nem tudsz szerkeszteni.')

        await ctx.send(ctx.author.mention, embed=embed)

    @kartya.error
    async def kartya_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg Tier-t, nevet vagy leírást.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb ppreward add kartya <tier> "név" "leírás"`'
            )

            await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def season(self, ctx):

        season = dbload('seasons')[str(ctx.guild.id)]

        if season['isOn']:
            embed = discord.Embed(title=season['name'],
                                  description='A Season részletei',
                                  color=0x8a7c74)

            embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                             icon_url=ctx.author.avatar_url)

            embed.add_field(name='Időtartam',
                            value=season['date'],
                            inline=False)
            role = ctx.guild.get_role(season['role'])
            embed.add_field(name='Rang',
                            value=role.mention,
                            inline=False)
            embed.add_field(name='Ár',
                            value='{} <:plancoin:799180662166781992>'.format(season['price']),
                            inline=False)

        else:
            embed = newErr('Nincs aktív season')

        await ctx.send(ctx.author.mention, embed=embed)

    @season.command(aliases=['date', 'dátum'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def datum(self, ctx, date: str):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']

        if not isOn:
            try:
                seasons = dbload('seasons')

                time = datetime.strptime(str(date), '%Y-%m-%d')

                if time < datetime.now() + timedelta(weeks=3):
                    embed = newErr('Helytelen időt adtál meg.')
                    embed.add_field(name='Információ:',
                                    value="A Season-nek legalább 1 hónap hosszúnak kell lennie.")
                    await ctx.send(embed=embed)

                else:
                    seasons[str(ctx.guild.id)]['date'] = str(time)
                    embed = discord.Embed(title='Season hossza beállítva',
                                          description='A következő season vége: {}'.format(str(time)),
                                          color=0x8a7c74)

                    embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                                     icon_url=ctx.author.avatar_url)

                dbsave(seasons, 'seasons')

            except:
                embed = newErr('Helytelen időt adtál meg.')
                embed.add_field(
                    name='Helyes formátum:',
                    value='év-hónap-nap\n*2021-09-29*'
                )

        else:
            embed = newErr('Aktív Season-t nem tudsz szerkeszteni.')

        await ctx.send(ctx.author.mention, embed=embed)

    @datum.error
    async def datum_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg dátumot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb season datum "év-hónap-nap"`'
            )

            await ctx.send(embed=embed)

    @season.command(aliases=['név', 'name'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def nev(self, ctx, name: str):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']
        if not isOn:
            seasons = dbload('seasons')

            name = name.replace('_', ' ')
            seasons[str(ctx.guild.id)]['name'] = name

            embed = discord.Embed(title='Season neve beállítva',
                                  description='A következő season neve: {}'.format(name),
                                  color=0x8a7c74)

            embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                             icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

            dbsave(seasons, 'seasons')
        else:
            embed = newErr('Aktív Season-t nem tudsz szerkeszteni.')

        await ctx.send(ctx.author.mention, embed=embed)

    @nev.error
    async def nev_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg nevet.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb season nev "név"`'
            )

            await ctx.send(embed=embed)

    @season.command(aliases=['role'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def rang(self, ctx, role: discord.Role):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']
        if not isOn:
            if not role.is_bot_managed():
                seasons = dbload('seasons')

                seasons[str(ctx.guild.id)]['role'] = role.id

                embed = discord.Embed(title='Season rang beállítva',
                                      description='A következő season rangja: {}'.format(role.name),
                                      color=0x8a7c74)

                embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                                 icon_url=ctx.author.avatar_url)

                dbsave(seasons, 'seasons')

            else:
                embed = newErr('Ez a rang Bot exkluzív.')
                embed.add_field(
                    name='Adj meg másik rangot',
                    value='** **'
                )
        else:
            embed = newErr('Aktív Season-t nem tudsz szerkeszteni.')

        await ctx.send(ctx.author.mention, embed=embed)

    @rang.error
    async def rang_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg rangot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb season rang <@rang>`'
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
                value='`!pb season rang <@rang>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @season.command(aliases=['siderole'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def mellekrang(self, ctx, role: discord.Role):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']
        if not isOn:
            if not role.is_bot_managed():
                seasons = dbload('seasons')

                seasons[str(ctx.guild.id)]['siderole'] = role.id

                embed = discord.Embed(title='Season rang beállítva',
                                      description='A következő season mellék rangja: {}'.format(role.name),
                                      color=0x8a7c74)

                embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                                 icon_url=ctx.author.avatar_url)

                dbsave(seasons, 'seasons')

            else:
                embed = newErr('Ez a rang Bot exkluzív.')
                embed.add_field(
                    name='Adj meg másik rangot',
                    value='** **'
                )
        else:
            embed = newErr('Aktív Season-t nem tudsz szerkeszteni.')

        await ctx.send(ctx.author.mention, embed=embed)

    @mellekrang.error
    async def rang_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg rangot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb season mellekrang <@rang>`'
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
                value='`!pb season mellekrang <@rang>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @season.command(aliases=['price', 'ár'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def ar(self, ctx, price: int):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']
        if not isOn:
            seasons = dbload('seasons')

            seasons[str(ctx.guild.id)]['price'] = price

            embed = discord.Embed(title='PlankPass ára beállítva',
                                  description='A következő PlankPass ára: {}'.format(price),
                                  color=0x8a7c74)

            embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                             icon_url=ctx.author.avatar_url)

            dbsave(seasons, 'seasons')
        else:
            embed = newErr('Aktív Season-t nem tudsz szerkeszteni.')

        await ctx.send(ctx.author.mention, embed=embed)

    @ar.error
    async def ar_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg árat.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb season ar <ár>`'
            )

            await ctx.send(embed=embed)

    @season.command(aliases=['start'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def kezd(self, ctx):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']

        if not isOn:
            seasons = dbload('seasons')

            if seasons[str(ctx.guild.id)]['date'] == "":
                embed = newErr('Nincs beállítva a season hossza.')
                await ctx.send(embed=embed)

            elif seasons[str(ctx.guild.id)]['name'] == "":
                embed = newErr('Nincs beállítva a season neve.')
                await ctx.send(embed=embed)

            elif seasons[str(ctx.guild.id)]['role'] == "":
                embed = newErr('Nincs beállítva a season rangja.')
                await ctx.send(embed=embed)

            elif seasons[str(ctx.guild.id)]['price'] == -1:
                embed = newErr('Nincs megadva a PlankPass ára.')
                await ctx.send(embed=embed)

            else:

                embed = discord.Embed(
                    title='Biztosan elkezded a Seasont?',
                    description='Kezdés előtt ajánlatos megnézni a Tier ajándékokat, mivel kezdés után nem tudod módosítani.',
                    color=0x8a7c74
                )

                embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                                 icon_url=ctx.author.avatar_url)

                embed.add_field(
                    name='Ha készen állsz írd be',
                    value='Igen'
                )

                embed.set_footer(
                    text='Válaszodra 5 másodperc áll rendelkezésre'
                )

                msg = await ctx.send(ctx.author.mention, embed=embed)

                def check(m):
                    return m.channel == ctx.channel and m.content.lower() == 'igen' and m.author == ctx.author

                try:
                    ready = await self.bot.wait_for('message', timeout=5, check=check)

                    if ready:
                        embed = discord.Embed(title='Season elkezdve',
                                              description='Elindítottad a {} Season-t'.format(
                                                  seasons[str(ctx.guild.id)]['name']),
                                              color=0x00b000)

                        embed.set_author(name=ctx.guild.owner,
                                         url=f'https://discord.com/users/{ctx.guild.owner.id}',
                                         icon_url=ctx.guild.owner.avatar_url)

                        seasons[str(ctx.guild.id)]['isOn'] = True

                        dbsave(seasons, 'seasons')

                        await msg.edit(embed=embed)

                except:
                    embed = newErr('Letelt a döntés idő.')
                    embed.add_field(
                        name='A season nem lett elindítva',
                        value='** **'
                    )
                    await ctx.send(ctx.author.mention, embed=embed)
        else:
            embed = newErr('Aktív Season-t nem tudsz újra elkezdeni.')
            await ctx.send(ctx.author.mention, embed=embed)

    @season.command(aliases=['stop', 'leállít'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def leallit(self, ctx):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']

        if isOn:
            seasons = dbload('seasons')

            seasons[str(ctx.guild.id)]['isOn'] = False

            embed = discord.Embed(
                title='Season megállítva',
                description='A Season-t bármikor újra indíthatod',
                colour=0xb80000
            )

            embed.set_author(name=ctx.guild.owner,
                             url=f'https://discord.com/users/{ctx.guild.owner.id}',
                             icon_url=ctx.guild.owner.avatar_url)

            embed.add_field(
                name='Leállítottad a Season-t',
                value='** **',
                inline=False
            )

            embed.add_field(
                name='Újra indításhoz írd',
                value='`!pb season kezd`',
                inline=False
            )

            dbsave(seasons, 'seasons')

        else:
            embed = newErr('Nincs aktív season.')

        await ctx.send(embed=embed)

    @season.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def kikapcsol(self, ctx):
        isOn = dbload('seasons')[str(ctx.guild.id)]['isOn']

        if isOn:
            try:
                seasons = dbload('seasons')

                embed = discord.Embed(
                    title='Season kikapcsolása',
                    description='Biztosan kikapcsolod a Season-t?\n'
                                'Ezzel elveszed mindenki PlankPass-ét és mindenki Tiere 0 lesz.\n'
                                'Ezt nem vonhatod vissza.',
                    colour=0x8a7c74
                )

                embed.add_field(
                    name='Ha készen állsz írd',
                    value='Igen'
                )

                embed.set_footer(
                    text='Válaszodra 5 másodperc van'
                )

                msg = await ctx.send(embed=embed)

                def check(m):
                    return m.content.lower() == 'igen' and m.author == ctx.author

                choice = await self.bot.wait_for('message', check=check, timeout=5)

                if choice:
                    embed = discord.Embed(
                        title='Season leállítva',
                        description='Leállítottad a Season-t.',
                        colour=0xff0000
                    )

                    server = ctx.guild.id

                    pusers = dbload('premiumusers')
                    users = dbload('users')

                    for user in pusers[str(server)].copy():
                        del pusers[str(server)][user]

                    for user in users[str(server)]:
                        users[str(server)][user]['plankpass'] = False

                    dbsave(pusers, 'premiumusers')
                    dbsave(users, 'users')
                    del pusers
                    del users

                    del seasons[str(server)]['rewards']
                    seasons[str(server)]['rewards'] = {}
                    for i in range(1, 41):
                        seasons[str(server)]['rewards'][str(i)] = {}

                    seasons[str(server)]["isOn"] = False
                    seasons[str(server)]["name"] = ""
                    seasons[str(server)]["date"] = ""
                    seasons[str(server)]["role"] = ""
                    seasons[str(server)]["price"] = -1

                    dbsave(seasons, 'seasons')

                    await msg.edit(embed=embed)

            except:
                embed = newErr('Letelt a választási idő')
                embed.add_field(
                    name='A Season nem lett kikapcsolva',
                    value='** **'
                )

                await ctx.send(embed=embed)

        else:
            embed = newErr('Nincs aktív season.')
            await ctx.send(embed=embed)


def dbload(name: str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)


def dbsave(db, name: str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)


async def update_db(self, db, user, serverId):
    if f'{serverId}' not in db:
        db[f'{serverId}'] = {}
    if f'{user.id}' not in db[f'{serverId}']:
        db[f'{serverId}'][f'{user.id}'] = {}
        db[f'{serverId}'][f'{user.id}']['exp'] = 0
        db[f'{serverId}'][f'{user.id}']['lvl'] = 0


async def addExp(self, db, user, server):
    serverId = server.id
    lvlCurrent = db[f'{serverId}'][f'{user.id}']['lvl']

    if str(user.id) in db[str(serverId)]:
        users = dbload('users')
        users[str(server.id)][str(user.id)]['plankpass'] = True
        dbsave(users, 'users')

    if lvlCurrent < 40:
        db[f'{serverId}'][f'{user.id}']['exp'] += randint(5, 10)
        lvlUpXp = 40 * lvlCurrent * lvlCurrent - 30 * lvlCurrent

        if db[f'{serverId}'][f'{user.id}']['exp'] >= lvlUpXp:
            pfx = dbload('prefixes')
            reward = dbload('seasons')[str(serverId)]['rewards'][str(lvlCurrent + 1)]

            db[str(serverId)][str(user.id)]['lvl'] += 1

            embed = discord.Embed(title='Tier lépés', description="", color=0x8a7c74)
            embed.set_author(name=user, url="https://discord.com/users/{}".format(user.id))
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name='Új tier: ', value=lvlCurrent + 1, inline=False)

            if hasPP(user, server):
                if not len(reward) == 0:
                    if reward['type'] == 'role':
                        role = server.get_role(reward["id"])
                        if role is not None:
                            embed.add_field(name='Megkaptad a következő rangot', value=role.mention, inline=False)
                            await user.add_roles(role)
                        else:
                            print('Season rang hiba... {}'.format(reward["id"]))
                            embed.add_field(name='Hiba történt.',
                                            value="Nem kaptad meg a rangot. Kérlek ezt jelezd egy szerver admin felé.")
                        embed.add_field(name='Megkaptad a következő rangot', value=role.mention, inline=False)
                    elif reward['type'] == 'bal':
                        users = dbload('users')
                        users[str(serverId)][str(user.id)]['bal'] += reward['amount']
                        dbsave(users, 'users')
                        embed.add_field(name='Kaptál',
                                        value='{}<:plancoin:799180662166781992>'.format(reward['amount']), inline=False)
                    elif reward['type'] == "card":
                        users = dbload('users')
                        id = reward['id']
                        name = reward['name']
                        desc = reward['desc']
                        users[str(serverId)][str(user.id)]['cards'][id] = {}
                        users[str(serverId)][str(user.id)]['cards'][id]['name'] = name
                        users[str(serverId)][str(user.id)]['cards'][id]['desc'] = desc
                        users[str(serverId)][str(user.id)]['cards'][id]['id'] = id
                        dbsave(users, 'users')
                        embed.add_field(name='Speciális kártya elérve', value='{}\n{}'.format(name, desc), inline=False)

                channel = None
                isChnl = False

                if 'lvlChnl' in pfx[f'{serverId}']:
                    channel = self.bot.get_channel(pfx[f'{serverId}']['lvlChnl'])
                    isChnl = True

                del pfx

                if isChnl == True:
                    await channel.send(user.mention, embed=embed)


def hasPP(user: discord.Member, server: discord.Guild):
    users = dbload('users')

    if users[str(server.id)][str(user.id)]['plankpass']:
        return True
    else:
        return False


def newErr(reason: str):
    embed = discord.Embed(title='Hiba', description=reason, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed


def setup(bot):
    bot.add_cog(SeasonSystem(bot))
