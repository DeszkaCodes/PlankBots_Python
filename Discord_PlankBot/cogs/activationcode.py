import discord
from discord.ext import commands
import json
from random import randint

def isMe(ctx):
    return ctx.author.id == 216965188606361611

class CodeSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Code System Cog Online')

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def code(self, ctx, code : str):
        if len(code) == 12:
            codes = dbload('codes')

            if code in codes['codes']:
                if codes['codes'][code]['uses'] == 0:
                    embed=newErr('Ezt a kódot már nem lehet többször felhasználni.')
                    del codes['codes'][code]
                else:
                    if ctx.author.id not in codes['codes'][code]['usedBy']:
                        if codes['codes'][code]['type'] == 'money':
                            moneyChange(self, ctx.author, ctx.guild.id, codes['codes'][code]['amount'])
                            codes['codes'][code]['uses'] -= 1
                            embed = discord.Embed(
                                title='Kód aktiválva',
                                color=0x8a7c74
                            )
                            embed.set_author(
                                name=ctx.author,
                                url="https://discord.com/users/{}".format(ctx.author.id),
                                icon_url=ctx.author.avatar_url
                            )

                            embed.add_field(
                                name='Aktiválva',
                                value='PlanCoin',
                                inline=False
                            )
                            embed.add_field(
                                name='Összeg',
                                value='{:,} <:plancoin:799180662166781992>'.format(codes['codes'][code]['amount']),
                                inline=False
                            )

                        elif codes['codes'][code]['type'] == 'role':

                            role = ctx.guild.get_role(codes['codes'][code]['id'])

                            if role == None:
                                raise commands.errors.RoleNotFound('')

                            await ctx.author.add_roles(role)

                            codes['codes'][code]['uses'] -= 1

                            embed = discord.Embed(
                                title='Kód aktiválva',
                                color=0x8a7c74
                            )
                            embed.set_author(
                                name=ctx.author,
                                url="https://discord.com/users/{}".format(ctx.author.id),
                                icon_url=ctx.author.avatar_url
                            )

                            embed.add_field(
                                name='Aktiválva',
                                value='Szerver rang',
                                inline=False
                            )
                            embed.add_field(
                                name='Rang',
                                value=role.mention,
                                inline=False
                            )

                        elif codes['codes'][code]['type'] == 'card':

                            if codes['codes'][code]['server'] == ctx.guild.id:
                                codes['codes'][code]['uses'] -= 1

                                name = codes['codes'][code]['name']
                                desc = codes['codes'][code]['desc']

                                users = dbload('users')

                                id = randint(5001, 10000)
                                while id in users[str(ctx.guild.id)][str(ctx.author.id)]['cards']:
                                    id = randint(5001, 10000)

                                users[str(ctx.guild.id)][str(ctx.author.id)]['cards'][str(id)] = {}
                                users[str(ctx.guild.id)][str(ctx.author.id)]['cards'][str(id)]['name'] = name
                                users[str(ctx.guild.id)][str(ctx.author.id)]['cards'][str(id)]['desc'] = desc
                                users[str(ctx.guild.id)][str(ctx.author.id)]['cards'][str(id)]['id'] = id

                                dbsave(users, 'users')

                                embed = discord.Embed(
                                    title='Kód aktiválva',
                                    color=0x8a7c74
                                )
                                embed.set_author(
                                    name=ctx.author,
                                    url="https://discord.com/users/{}".format(ctx.author.id),
                                    icon_url=ctx.author.avatar_url
                                )

                                embed.add_field(
                                    name='Aktiválva',
                                    value='Lokális kártya',
                                    inline=False
                                )
                                embed.add_field(
                                    name='Név',
                                    value=name,
                                    inline=False
                                )
                                embed.add_field(
                                    name='Leírás',
                                    value=desc,
                                    inline=False
                                )
                            else:
                                embed = newErr('Ez a kártya nem erre a szerverre van.')

                        else:
                            codes['codes'][code]['uses'] -= 1

                            name = codes['codes'][code]['name']
                            desc = codes['codes'][code]['desc']

                            users = dbload('globalusers')

                            if str(ctx.author.id) not in users:
                              users[str(ctx.author.id)] = {}

                            id = randint(5001, 10000)
                            while id in users[str(ctx.author.id)]:
                                id = randint(5001, 10000)

                            users[str(ctx.author.id)][str(id)] = {}
                            users[str(ctx.author.id)][str(id)]['name'] = name
                            users[str(ctx.author.id)][str(id)]['desc'] = desc

                            dbsave(users, 'globalusers')

                            embed = discord.Embed(
                                title='Kód aktiválva',
                                color=0x8a7c74
                            )
                            embed.set_author(
                                name=ctx.author,
                                url="https://discord.com/users/{}".format(ctx.author.id),
                                icon_url=ctx.author.avatar_url
                            )

                            embed.add_field(
                                name='Aktiválva',
                                value='Univerzális kártya',
                                inline=False
                            )
                            embed.add_field(
                                name='Név',
                                value=name,
                                inline=False
                            )
                            embed.add_field(
                                name='Leírás',
                                value=desc,
                                inline=False
                            )

                        codes['codes'][code]['usedBy'].append(ctx.author.id)
                    else:
                        embed=newErr('Ezt a kódot már használtad 1x.')

            else:
                embed=newErr('Nem létezik ilyen kód.')

            dbsave(codes, 'codes')
        else:
            embed = newErr('A megadott kód nem 12 karakteres.')

        await ctx.send(ctx.author.mention, embed=embed)

    @code.error
    async def code_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtad meg a kódot.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb code <kód>`'
            )

            await ctx.send(embed=embed)

    @code.command()
    @commands.guild_only()
    @commands.check(isMe)
    async def delete(self, ctx, code: str):
        codes = dbload('codes')

        del codes['codes'][code]

        dbsave(codes, 'codes')

        await ctx.send(
            'Deleted code {}'.format(code)
        )

    @code.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.check(isMe)
    async def new(self, ctx):
        await ctx.send(
            'money(amount, uses)\n'
            'role(role, uses)\n'
            'card(name,desc,serverid,universal:bool,uses)'
        )

    @new.command()
    @commands.guild_only()
    @commands.check(isMe)
    async def money(ctx, amount : int, uses : int):
        samples = (
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        )

        codes = dbload('codes')

        if uses == 0:
            uses = -1

        newCode = ''
        for i in range(12):
            newCode += samples[randint(0, len(samples) - 1)]

        while newCode in codes["codes"]:
            newCode = ''
            for i in range(1):
                newCode += samples[randint(0, len(samples) - 1)]

        codes['codes'][newCode] = {}
        codes['codes'][newCode]['type'] = 'money'
        codes['codes'][newCode]['amount'] = amount
        codes['codes'][newCode]['uses'] = uses
        codes['codes'][newCode]['usedBy'] = []

        dbsave(codes, 'codes')

        await ctx.send('kód: {}'.format(newCode))

    @new.command()
    @commands.guild_only()
    @commands.check(isMe)
    async def role(ctx, role : discord.Role, uses: int):

        samples = (
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        )

        codes = dbload('codes')

        if uses == 0:
            uses = -1

        newCode = ''
        for i in range(12):
            newCode += samples[randint(0, len(samples) - 1)]

        while newCode in codes["codes"]:
            newCode = ''
            for i in range(12):
                newCode += samples[randint(0, len(samples) - 1)]

        codes['codes'][newCode] = {}
        codes['codes'][newCode]['type'] = 'role'
        codes['codes'][newCode]['id'] = role.id
        codes['codes'][newCode]['uses'] = uses
        codes['codes'][newCode]['usedBy'] = []

        dbsave(codes, 'codes')

        await ctx.send('kód: {}'.format(newCode))

    @new.command()
    @commands.guild_only()
    @commands.check(isMe)
    async def card(ctx, name : str, desc : str, serverid : int, universal : bool, uses: int):
        samples = (
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        )

        codes = dbload('codes')

        if uses == 0:
            uses = -1

        newCode = ''
        for i in range(12):
            newCode += samples[randint(0, len(samples) - 1)]

        while newCode in codes["codes"]:
            newCode = ''
            for i in range(12):
                newCode += samples[randint(0, len(samples) - 1)]

        codes['codes'][newCode] = {}
        if not universal:
            codes['codes'][newCode]['type'] = 'card'
        else:
            codes['codes'][newCode]['type'] = 'ucard'
        codes['codes'][newCode]['server'] = serverid
        codes['codes'][newCode]['name'] = name
        codes['codes'][newCode]['desc'] = desc
        codes['codes'][newCode]['uses'] = uses
        codes['codes'][newCode]['usedBy'] = []

        dbsave(codes, 'codes')

        await ctx.send('kód: {}'.format(newCode))


    @code.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.check(isMe)
    async def masscreate(self, ctx):
        await ctx.send(
            'money(amount, createAmount)\n'
            'role(role, createAmount)\n'
            'card(name, desc, serverid, universal:bool, createAmount)'
        )

    @masscreate.command()
    @commands.guild_only()
    @commands.check(isMe)
    async def money(self, ctx, amount: int, createAmount : int):
        samples = (
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        )

        codes = dbload('codes')

        strCodes = ''

        uses = 1

        for i in range(createAmount):
            newCode = ''
            for i in range(12):
                newCode += samples[randint(0, len(samples) - 1)]

            while newCode in codes["codes"]:
                newCode = ''
                for i in range(1):
                    newCode += samples[randint(0, len(samples) - 1)]

            strCodes += '{}\n'.format(newCode)

            codes['codes'][newCode] = {}
            codes['codes'][newCode]['type'] = 'money'
            codes['codes'][newCode]['amount'] = amount
            codes['codes'][newCode]['uses'] = uses
            codes['codes'][newCode]['usedBy'] = []

        dbsave(codes, 'codes')

        await ctx.send('kód:\n{}'.format(strCodes))

    @masscreate.command()
    @commands.guild_only()
    @commands.check(isMe)
    async def role(self, ctx, role: discord.Role, createAmount : int):

        samples = (
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        )

        codes = dbload('codes')

        strCodes = ''

        uses = 1


        for i in range(createAmount):
            newCode = ''
            for i in range(12):
                newCode += samples[randint(0, len(samples) - 1)]

            while newCode in codes["codes"]:
                newCode = ''
                for i in range(12):
                    newCode += samples[randint(0, len(samples) - 1)]

            strCodes += '{}\n'.format(newCode)

            codes['codes'][newCode] = {}
            codes['codes'][newCode]['type'] = 'role'
            codes['codes'][newCode]['id'] = role.id
            codes['codes'][newCode]['uses'] = uses
            codes['codes'][newCode]['usedBy'] = []

        dbsave(codes, 'codes')

        await ctx.send('kód:\n{}'.format(strCodes))

    @masscreate.command()
    @commands.guild_only()
    @commands.check(isMe)
    async def card(self, ctx, name: str, desc: str, serverid: int, universal: bool, createAmount : int):
        samples = (
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        )

        codes = dbload('codes')

        strCodes = ''

        uses = 1

        for i in range(createAmount):
            newCode = ''
            for i in range(12):
                newCode += samples[randint(0, len(samples) - 1)]

            while newCode in codes["codes"]:
                newCode = ''
                for i in range(12):
                    newCode += samples[randint(0, len(samples) - 1)]

            strCodes += '{}\n'.format(newCode)

            codes['codes'][newCode] = {}
            if not universal:
                codes['codes'][newCode]['type'] = 'card'
            else:
                codes['codes'][newCode]['type'] = 'ucard'
            codes['codes'][newCode]['server'] = serverid
            codes['codes'][newCode]['name'] = name
            codes['codes'][newCode]['desc'] = desc
            codes['codes'][newCode]['uses'] = uses
            codes['codes'][newCode]['usedBy'] = []

        dbsave(codes, 'codes')

        await ctx.send('kód:\n{}'.format(strCodes))


def dbload(name : str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)

def dbsave(db, name : str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)

def rounder(num, amount):
    num = int(num / amount) * amount
    return num

def moneyChange(self, user : discord.User, serverId, amount):
    users = dbload('users')

    users[f'{serverId}'][f'{user.id}']['bal'] += amount

    dbsave(users, 'users')

def newErr(reason : str):
    embed=discord.Embed(title='Hiba', description=reason, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed

def balance(self, user: discord.User, server):
    users = dbload('users')
    return users[f'{server}'][f'{user.id}']['bal']

def setup(bot):
    bot.add_cog(CodeSystem(bot))