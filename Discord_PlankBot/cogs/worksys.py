import discord
from discord.ext import commands
from random import randint, random
import json

class WorkSystem(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    timetable = {'minute': 60, 'hour': 3600, 'day': 86400, 'week': 604800,
                 'month': 2592000}

    @commands.Cog.listener()
    async def on_ready(self):
        print('Work System Cog Online')

#MUNKA--------------------------------------------------------------------------
    @commands.command(aliases = ['work'])
    @commands.guild_only()
    @commands.cooldown(1, timetable['minute']*5, commands.BucketType.member)
    async def munka(self, ctx):
        money = rounder(randint(1000,5000), 100)
        moneyChange(self, ctx.author, ctx.guild.id, money)
        embed=discord.Embed(title='Fizetés', description='Fizetség a szorgos munkádért.', color=0xC99B00)
        embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url='https://imgur.com/bekpJmK.png')
        embed.add_field(name='Fizetséged: ', value='{:,} <:plancoin:799180662166781992>'.format(money))
        embed.set_footer(text=f'Mielőtt megint dolgozni tudnál, várnod kell 5 percet.')
        await ctx.send(embed=embed)

    @commands.command(aliases = ['lopás', 'lop', 'rabol'])
    @commands.guild_only()
    @commands.cooldown(1, 30 * timetable['minute'], commands.BucketType.member)
    async def lopas(self, ctx):

        if random() < 0.5:
            money = rounder(randint(10000,15000), 1000)
            embed=discord.Embed(title='Sikeres lopás', description='Sikeresen kiraboltál egy házat.', color=0xC99B00)
            embed.set_thumbnail(url='https://imgur.com/aFJ5GQB.png')
            embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}', icon_url=ctx.author.avatar_url)
            embed.add_field(name='Zsákmányod értéke: ', value='{:,} <:plancoin:799180662166781992>'.format(money))
            embed.set_footer(text='Le kell lapulnod amíg folyik a nyomozás, fél óra múlva újra próbálkozhatsz.')
        else:
            money = rounder(randint(-15000,-10000), 1000)
            embed=discord.Embed(title='Sikertelen lopás', description='Megszólalt a riasztó és otthagytad a felszerelésed.', color=0xC99B00)
            embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}', icon_url=ctx.author.avatar_url)
            embed.add_field(name='Elbukott pénz: ', value='{:,} <:plancoin:799180662166781992>'.format(money))
            embed.set_footer(text='Le kell lapulnod amíg folyik a nyomozás, fél óra múlva újra próbálkozhatsz.')
            embed.set_thumbnail(url='https://imgur.com/Lqltz9R.png')

        moneyChange(self, ctx.author, ctx.guild.id, money)
        await ctx.send(embed=embed)

    @commands.command(aliases=['bigwork', 'túlóra'])
    @commands.guild_only()
    @commands.cooldown(1, 1.5 * timetable['hour'], commands.BucketType.member)
    async def tulora(self, ctx):
        payment = rounder(randint(30000, 50000), 1000)

        moneyChange(self, ctx.author, ctx.guild.id, payment)

        embed = discord.Embed(title='Bónusz', description='A túlórád nem marad jutalom nélkül.', color=0xC99B00)
        embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                         icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url='https://imgur.com/bekpJmK.png')
        embed.add_field(name='Bónuszod: ', value='{:,} <:plancoin:799180662166781992>'.format(payment))
        embed.set_footer(text=f'Mielőtt megint túlórázni tudnál, várnod kell 1 órát.')

        await ctx.send(embed=embed)

    @commands.command(aliases=['segély'])
    @commands.guild_only()
    @commands.cooldown(1, timetable['hour'], commands.BucketType.member)
    async def segely(self, ctx):

        bal = balance(self, ctx.author, ctx.guild.id)

        segely = int(-bal*0.95)

        if bal < 0:
            moneyChange(self, ctx.author, ctx.guild.id, segely)
            embed = discord.Embed(
                title='Segély felvéve',
                description='Elmentél **{}** hivataljába és felvetted a tartozás segélyt.'.format(ctx.guild.name),
                color=0x8a7c74
            )
            embed.set_author(name=ctx.author,
                             url="https://discord.com/users/{}".format(ctx.author.id))
            embed.set_thumbnail(url=ctx.author.avatar_url)

            embed.set_footer(
                text='A következő 12 óráig nem vehetsz fel újabb segélyt.'
            )

            embed.add_field(
                name='Kifizetett tartozás',
                value='{:,} <:plancoin:799180662166781992>'.format(segely),
                inline=False
            )

        else:
            ctx.command.reset_cooldown(ctx)
            embed=newErr('Nem vagy tartozásban.')

        await ctx.send(ctx.author.mention, embed=embed)


def dbload(name : str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)

def dbsave(db, name : str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)

def rounder(num, amount):
    num = int(num / amount) * amount
    return num

def moneyChange(self, user : discord.User, server, amount):
    users = dbload('users')

    users[f'{server}'][f'{user.id}']['bal'] += amount

    dbsave(users, 'users')

def newErr(reason : str):
    embed=discord.Embed(title='Hiba', description=reason, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed

def balance(self, user: discord.User, server):
    users = dbload('users')
    return users[f'{server}'][f'{user.id}']['bal']

def setup(bot):
    bot.add_cog(WorkSystem(bot))
