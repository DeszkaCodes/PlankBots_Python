import os
import discord
from discord.ext import commands, tasks
from itertools import cycle
from random import randint
import json

token = 'NzkxNzYxMTI5ODAxMzg0MDA2.X-T3Aw.czYUpzJgQBDwcY4JDO5JK9k0aIk'
testToken = 'ODEzMDg2NTkzMTc5MDU4MjA2.YDKL5g.8LHA4pQF1hoR5wwWnRohDJJvNtw'

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!pb ", guild_subscriptions=True, intents=intents)
bot.remove_command('help')
os.chdir("./")

status = cycle(('!pb help', '!pb invite'))


# -------------------------------------------------------------------------------
@bot.event
async def on_ready():
    status_change.start()
    print("Bot Online")


@tasks.loop(seconds=10)
async def status_change():
    await bot.change_presence(activity=discord.Game(next(status)))


# -------------------------------------------------------------------------------

@bot.event
async def on_member_join(member):
    pfx = dbload('prefixes')[str(member.guild.id)]

    if 'welcomeChnl' in pfx:
        if not member.bot:
            channel = bot.get_channel(pfx['welcomeChnl'])
            del pfx
            await channel.send('{} csatlakozott a szerverhez!'.format(member.mention))
        else:
            channel = bot.get_channel(pfx['welcomeChnl'])
            del pfx
            await channel.send('{} bot elérkezett segíteni a moderátorok munkáját.'.format(member.mention))


# -------------------------------------------------------------------------------
# USER COMMANDS
@bot.command(aliases=['meghív', 'meghívó'])
async def invite(ctx):
    embed = discord.Embed(
        title='Információ',
        description='A Bot összes funkciója és meghívó link.',
        color=0x8a7c74
    )
    embed.set_thumbnail(
        url=str(bot.user.avatar_url)[:-15]
    )
    embed.add_field(
        name='Moderációs rendszer',
        value='-Üzenetek törlése'
              '\n-Tag kirúgása'
              '\n-Tag némítása',
        inline=False
    )
    embed.add_field(
        name='Pénz rendszer',
        value='-Pénz utalása'
              '\n-Pénz adás (administrator)'
              '\n-Egyenleg megnézése',
        inline=False
    )
    embed.add_field(
        name='Bolt rendszer',
        value='-Rangok vásárlása'
              '\n-Kártyák vásárlása',
        inline=False
    )
    embed.add_field(
        name='Kártya rendszer',
        value='-Különleges kártyák'
              '\n-Kártyák adása'
              '\n-Kártyák elvétele'
              '\n-A kártyáknak van nevük és leírásuk, mely egyénileg írható.',
        inline=False
    )
    embed.add_field(
        name='PlankPass rendszer',
        value='-Megadott ideig tart'
              '\n-40 Tier'
              '\n-Tierenként beállítható rewardok',
        inline=False
    )
    embed.add_field(
        name='Munka/Szerencsejáték rendszer',
        value='-Lottó'
              '\n-Munka/Lopás'
              '\n-Roulette'
              '\n-Slotmachine',
        inline=False
    )
    embed.add_field(
        name='Meghívó',
        value='https://discord.com/api/oauth2/authorize?client_id=791761129801384006&permissions=8&scope=bot',
        inline=False
    )

    await ctx.author.send(embed=embed)


@bot.command(aliases=['boosts'])
@commands.guild_only()
async def booster(ctx):

    premiumMembers = ctx.guild.premium_subscribers

    boosters = ''
    index = len(premiumMembers)-1

    while index > 0:
        boosters += '{}\n'.format(premiumMembers[index].name)
        index -= 1

    embed = discord.Embed(
        title='A szerver támogatói',
        name='Ezek a tagok Boost-olják a szervert.',
        color=0xFF73FA
    )

    embed.set_author(
        name=ctx.guild.name,
        icon_url=ctx.guild.icon_url
    )

    embed.set_thumbnail(
        url='https://imgur.com/KccGk03.png'
    )

    if len(boosters) == 0:
        embed.add_field(
            name='Nincs Booster ezen a szerveren',
            value='** **'
        )

        embed.set_footer(
            text='Ha támogatni akarod a szervert, nyomass egy Boost-ot.'.format(ctx.guild.owner.name)
        )

    elif len(boosters) > 800:
        embed.add_field(
            name='A szerveren {} Booster van'.format(len(premiumMembers)),
            value='Nem tudjuk kiírni a listát, mivel túl hosszú.'
        )
        embed.set_footer(
            text='Köszönjük szépen {} nevében is.'.format(ctx.guild.owner.name)
        )

    else:
        embed.add_field(
            name='A szerveren {} Booster van.'.format(len(premiumMembers)),
            value=boosters
        )

        embed.set_footer(
            text='Köszönjük szépen {} nevében is.'.format(ctx.guild.owner.name)
        )

    await ctx.send(ctx.author.mention, embed=embed)


# -------------------------------------------------------------------------------


# CONFIG COMMANDS
def dbload(name: str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)


def dbsave(db, name: str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)


def isMe(ctx):
    return ctx.author.id == 216965188606361611


def newErr(desc: str):
    embed = discord.Embed(title='Hiba', description=desc, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed


@bot.command()
@commands.check(isMe)
async def clearcon(ctx):
    print(
        '\n\n\n\n\n<=======================>\n\n\n\n\n'
    )


@bot.command()
@commands.check(isMe)
async def printdb(ctx, db: str):
    with open(db, 'r') as f:
        db = json.load(f)

    await ctx.send(db)


@bot.command()
@commands.check(isMe)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} loaded.')


#
@bot.command()
@commands.check(isMe)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} unloaded.')


@bot.command()
@commands.check(isMe)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} reloaded.')


@bot.group(invoke_without_command=True)
@commands.check(isMe)
async def globalusers(ctx):
    users = dbload('globalusers')

    await ctx.send(users)


@globalusers.command()
@commands.check(isMe)
async def add(ctx, user: discord.User, name: str, desc: str):
    users = dbload('globalusers')

    if not str(user.id) in users:
        users[str(user.id)] = {}

    id = randint(0, 256)

    while id in users[str(user.id)]:
        id = randint(0, 256)

    users[str(user.id)][str(id)] = {}
    users[str(user.id)][str(id)]['name'] = name
    users[str(user.id)][str(id)]['desc'] = desc

    dbsave(users, 'globalusers')

    await ctx.send('{} added to Global Users with {} {}'.format(user, name, desc))


@globalusers.command()
@commands.check(isMe)
async def remove(ctx, user: discord.User, id: int):
    users = dbload('globalusers')

    del users[str(user.id)][str(id)]

    dbsave(users, 'globalusers')

    await ctx.send('Card {} deleted from user {}'.format(id, user))


@bot.command()
@commands.guild_only()
@commands.check(isMe)
async def debugfizet(ctx, user: discord.User, amount: int):
    users = dbload('users')

    users[f'{ctx.message.guild.id}'][f'{user.id}']['bal'] += amount
    await ctx.channel.send(f'{ctx.author.mention} - {amount} jóváírva {user.mention}-nak/nek.')

    dbsave(users, 'users')


# -------------------------------------------------------------------------------
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(testToken)
