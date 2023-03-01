import discord
from discord.ext import commands, tasks
import json
from datetime import datetime, timedelta
from termcolor import colored
import colorama

colorama.init()

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_db.start()
        print('Moderation Cog Online')

    @tasks.loop(minutes = 10)
    async def check_db(self):
        muted = dbload('mutes')

        pfx = dbload('prefixes')

        print(colored('\nUpdate time:{}'.format(datetime.now()), 'green'))

        try:
            for server in muted.copy():
                guild = self.bot.get_guild(int(server))
                for id in muted[server].copy():
                    stripdate = datetime.strptime(muted[server][id], '%Y-%m-%d %H:%M:%S.%f')
                    if stripdate < datetime.now():
                        user = guild.get_member(int(id))
                        role = guild.get_role(pfx[server]['mutedRole'])
                        await user.remove_roles(role)
                        del muted[server][id]
            print(colored('Muted Database updated', 'green'))

        except Exception as e:
            print(colored('Muted Database couldn\'t be updated:\n\t{}'.format(e), 'yellow'))

        dbsave(muted, 'mutes')


    @commands.command(aliases = ['töröl', 'tisztít'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 10):
        await ctx.channel.purge(limit = amount+1)
        await ctx.send(f'{amount} üzenet törölve.')

    @commands.command(aliases = ['némit', 'nemit'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, user : discord.Member, time : int, reason : str = 'Nincs megadva.'):
        pfx = dbload('prefixes')

        if time >= 10:
            if 'mutedRole' in pfx[f'{ctx.guild.id}']:
                muted = dbload('mutes')
                if str(ctx.guild.id) not in muted:
                    muted[str(ctx.guild.id)] = {}
                if str(user.id) not in muted:
                    muted[str(ctx.guild.id)][str(user.id)] = {}

                role = ctx.guild.get_role(pfx[str(ctx.guild.id)]['mutedRole'])

                date = datetime.now() + timedelta(minutes=time)

                muted[f'{ctx.guild.id}'][f'{user.id}'] = str(date)

                await user.add_roles(role)

                recieve=discord.Embed(
                    title='Lenémítottak',
                    color=0x8a7c74
                )

                recieve.set_author(
                    name=ctx.guild.name,
                    icon_url=ctx.guild.icon_url
                )

                recieve.add_field(
                    name='Admin',
                    value=ctx.author.mention,
                    inline=True
                )
                recieve.add_field(
                    name='Időtartam',
                    value='{} perc'.format(time),
                    inline=True
                )
                recieve.add_field(
                    name='Indok',
                    value=reason,
                    inline=False
                )

                await user.send(embed=recieve)

                embed=discord.Embed(
                    title="Felhasználó némítva",
                    description=f'{ctx.author.mention} lenémította: {user.mention}-t.',
                    color=0x8a7c74
                )

                embed.set_author(
                    name=ctx.author,
                    url=f'https://discord.com/users/{ctx.author.id}',
                    icon_url=ctx.author.avatar_url
                )

                embed.set_thumbnail(
                    url="https://imgur.com/SmB3JR8.png"
                )

                embed.add_field(
                    name='Admin',
                    value=ctx.author.mention,
                    inline=True
                )

                embed.add_field(
                    name='Időtartam',
                    value='{} perc'.format(time),
                )

                embed.add_field(
                    name='Indok',
                    value=reason,
                    inline=False
                )

                await ctx.send(embed=embed)
                with open('db/mutes.json', 'w') as f:
                    json.dump(muted, f)
            else:
                embed=newErr('Nincs megadva némított rang.')
                await ctx.send(embed=embed)
        else:
            embed=newErr('Minimum 10 percre kell lenémítani.')
            await ctx.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg egy értéket.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb mute <@tag> <percek> "indok"`'
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
                value='`!pb mute <@tag> <percek> "indok"`',
                inline=False
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, user : discord.Member):

        try:
            mutes = dbload('mutes')

            del mutes[str(ctx.guild.id)][str(user.id)]

            recieve = discord.Embed(
                title='Levették a némításodat',
                description='Egy moderátor/admin levette a némításod',
                colour=0x8a7c74
            )

            recieve.set_author(
                name=ctx.guild.name,
                icon_url=ctx.guild.icon_url
            )

            recieve.add_field(
                name='Admin',
                value=ctx.author.mention,
                inline=True
            )

            await user.send(embed=recieve)

            embed = discord.Embed(
                title='Némítás feloldva',
                colour=0x8a7c74
            )

            embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                             icon_url=ctx.author.avatar_url)

            embed.set_thumbnail(
                url='https://imgur.com/evRW4vO.png'
            )

            embed.add_field(
                name='Admin',
                value=ctx.author.mention,
                inline=True
            )

            embed.add_field(
                name='Felhasználó',
                value=user.mention
            )

            dbsave(mutes, 'mutes')

        except KeyError:
            embed = newErr('Ez a tag nincs lenémítva')

        await ctx.send(ctx.author.mention, embed=embed)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtad meg a tagot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb unmute <@tag>`'
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
                value='`!pb unmute <@tag>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: discord.Member, reason=None):
        pfx = dbload('prefixes')

        embed= discord.Embed(
            title='Tag kirúgva',
            color=0x8a7c74
        )

        embed.set_author(
            name=ctx.author,
            url=f'https://discord.com/users/{ctx.author.id}',
            icon_url=ctx.author.avatar_url
        )

        embed.set_thumbnail(
            url="https://imgur.com/Snff08x.png"
        )

        embed.add_field(
            name='Admin',
            value=ctx.author.name,
            inline=True
        )

        embed.add_field(
            name='Indok',
            value=reason,
            inline=False
        )

        if 'welcomeChnl' in pfx[f'{ctx.guild.id}']:
            channel = self.bot.get_channel(pfx[str(ctx.guild.id)]['welcomeChnl'])

            await channel.send(ctx.author.mention, embed=embed)
        else:
            await ctx.send(ctx.author.mention, embed=embed)

        await user.kick(reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtad meg kit akarsz kirúgni.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb kick <@tag> "indok"`'
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
                value='`!pb kick <@tag> "indok"`',
                inline=False
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, reason=None):
        pfx = dbload('prefixes')

        embed = discord.Embed(
            title='Tag kitiltva',
            color=0x8a7c74
        )

        embed.set_author(
            name=ctx.author,
            url=f'https://discord.com/users/{ctx.author.id}',
            icon_url=ctx.author.avatar_url
        )

        embed.set_thumbnail(
            url="https://imgur.com/9tb0dog.png"
        )

        embed.add_field(
            name='Admin',
            value=ctx.author.name,
            inline=True
        )

        embed.add_field(
            name='Indok',
            value=reason,
            inline=False
        )

        if 'welcomeChnl' in pfx[f'{ctx.guild.id}']:
            channel = self.bot.get_channel(pfx[str(ctx.guild.id)]['welcomeChnl'])

            await channel.send(ctx.author.mention, embed=embed)
        else:
            await ctx.send(ctx.author.mention, embed=embed)

        await user.ban(reason=reason)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtad meg kit akarsz kitiltani.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb ban <tag> "indok"`'
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
                value='`!pb ban <@tag> "indok"`',
                inline=False
            )
            await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def rang(self, ctx):


        embed = discord.Embed(
            title='Rang hozzáadása',
            description='Az indokot kettő idézőjel közé írd.',
            color=0x8a7c74
        )

        embed.add_field(
            name='Rang hozzáadása',
            value='`add <@tag> <@rang> "indok"`',
            inline=False
        )
        embed.add_field(
            name='Rang elvétele',
            value='`remove <@tag> <@rang> "indok"`',
            inline=False
        )

        await ctx.send(ctx.author.mention, embed=embed)

    @rang.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def ad(self, ctx, user : discord.Member, rang : discord.Role, reason = None):

        await user.add_roles(
            rang,
            reason=reason
        )

        embed = discord.Embed(
            title='Rang hozzáadva',
            description='Adtál egy rangot valakinek.',
            color=0x8a7c74
        )

        embed.set_author(
            name=ctx.author,
            url="https://discord.com/users/{}".format(ctx.author.id),
            icon_url=ctx.author.avatar_url
        )

        embed.add_field(
            name='Tag',
            value='{}'.format(user.mention)
        )

        embed.add_field(
            name='Adott rang',
            value='{}'.format(rang.mention)
        )

        if reason is not None:
            embed.add_field(
                name='Indok',
                value=reason,
                inline=False
            )

        await ctx.send(ctx.author.mention, embed=embed)

    @ad.error
    async def ad_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg tagot vagy rangot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb rang ad <@tag> <@rang> "indok"`'
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
                value='`!pb rang ad <@tag> <@rang>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @rang.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def elvesz(self, ctx, user : discord.Member, rang : discord.Role, reason = None):

        await user.remove_roles(
            rang,
            reason=reason
        )

        embed = discord.Embed(
            title='Rang elvéve',
            description='Elvettél egy rangot valakitől.',
            color=0x8a7c74
        )

        embed.set_author(
            name=ctx.author,
            url="https://discord.com/users/{}".format(ctx.author.id),
            icon_url=ctx.author.avatar_url
        )

        embed.add_field(
            name='Tag',
            value='{}'.format(user.mention)
        )

        embed.add_field(
            name='Elvett rang',
            value='{}'.format(rang.mention)
        )

        if reason is not None:
            embed.add_field(
                name='Indok',
                value=reason,
                inline=False
            )

        await ctx.send(ctx.author.mention, embed=embed)

    @elvesz.error
    async def elvesz_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg tagot vagy rangot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb rang elvesz <@tag> <@rang> "indok"`'
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
                value='`!pb rang elvesz <@tag> <@rang>`',
                inline=False
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=['rang-info'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def ranginfo(self, ctx, role : discord.Role):
        embed = discord.Embed(
            title = 'Rang Adatlap',
            color = role.color
        )

        embed.set_author(
            name=ctx.author,
            url=f'https://discord.com/users/{ctx.author.id}',
            icon_url=ctx.author.avatar_url
        )

        osszrang = len(ctx.guild.roles)
        embed.set_footer(
            text='Hely a rangok között {}/{}\n'
                 'Tagok: {}'.format(osszrang - role.position, osszrang, len(role.members))
        )

        embed.add_field(
            name='Név',
            value=role.name
        )

        embed.add_field(
            name='Azonosító (ID)',
            value=role.id
        )

        embed.add_field(
            name='Létrehozás dátum',
            value=role.created_at.strftime('%Y.%m.%d %H:%M'),
        )

        #NEWLINE
        if role.mentionable:
            embed.add_field(
                name='Megjelölhető',
                value='Igen'
            )
        else:
            embed.add_field(
                name='Megjelölhető',
                value='Nem'
            )

        embed.add_field(
            name='** **',
            value='** **'
        )

        if role.hoist:
            embed.add_field(
                name='Külön szedés',
                value='Igen'
            )
        else:
            embed.add_field(
                name='Külön szedés',
                value='Nem'
            )

        #NEWLINE
        if role.is_bot_managed():
            embed.add_field(
                name='Bot exkluzív',
                value='Igen'
            )
        else:
            embed.add_field(
                name='Bot exkluzív',
                value='Nem'
            )

        embed.add_field(
            name='** **',
            value='** **'
        )

        embed.add_field(
            name='Színkód',
            value='#%02x%02x%02x' % role.color.to_rgb()
        )


        await ctx.send(ctx.author.mention, embed=embed)

    @ranginfo.error
    async def ranginfo_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg rangot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb rang-info <@rang>`'
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
                value='`!pb ranginfo <@rang>`',
                inline=False
            )
            await ctx.send(embed=embed)

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
#-------------------------------------------------------------------------------
def setup(bot):
    bot.add_cog(Moderation(bot))
