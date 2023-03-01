import discord
from discord.ext import commands
import json
from random import randint

class LvlSystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Level System Cog Online')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        users = dbload('users')
        pfx = dbload('prefixes')[str(member.guild.id)]

        if not member.bot:
            await update_data(self, users, member, member.guild.id)
            if 'autoRole' in pfx:
                role = member.guild.get_role(dbload('prefixes')[str(member.guild.id)]['autoRole'])

                await member.add_roles(role, reason='Automatikus Tag rang')
        else:
            if 'botRole' in pfx:
                role = member.guild.get_role(dbload('prefixes')[str(member.guild.id)]['botRole'])

                await member.add_roles(role, reason='Automatikus Bot rang')

        dbsave(users, 'users')

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.channel.type) != 'private':
            if not message.author.bot:
                users = dbload('users')

                await update_data(self, users, message.author, message.guild.id)
                await add_exp(self, users, message.author, randint(5,10), message.guild.id)
                await lvl_up(self, users, message.author, message.guild.id)



                dbsave(users, 'users')


async def update_data(self, users, user, server):
    if f'{server}' not in users:
        users[f'{server}'] = {}
    if f'{user.id}' not in users[f'{server}']:
        users[f'{server}'][f'{user.id}'] = {}
        users[f'{server}'][f'{user.id}']['cards'] = {}
        users[f'{server}'][f'{user.id}']['exp'] = 0
        users[f'{server}'][f'{user.id}']['lvl'] = 0
        users[f'{server}'][f'{user.id}']['bal'] = 0
        users[f'{server}'][f'{user.id}']['plankpass'] = False

async def add_exp(self, users, user, exp, server):
    users[f'{server}'][f'{user.id}']['exp'] += exp

async def lvl_up(self, users, user, server):
    exp = users[f'{server}'][f'{user.id}']['exp']
    lvlCurrent = users[f'{server}'][f'{user.id}']['lvl']
    lvlUpXp = 10 * lvlCurrent * lvlCurrent - 10 * lvlCurrent

    if exp >= lvlUpXp:
        pfx = dbload('prefixes')

        channel = None
        isChnl = False

        if 'lvlChnl' in pfx[f'{server}']:
            channel = self.bot.get_channel(pfx[f'{server}']['lvlChnl'])
            isChnl = True

        del pfx

        embed=discord.Embed(title='Szintlépés', description="",color=0x8a7c74)
        embed.set_author(name=user, url="https://discord.com/users/{}".format(user.id))
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Új szint: ', value=lvlCurrent+1, inline = True)

        if isChnl == True:
            await channel.send(embed=embed)
        users[f'{server}'][f'{user.id}']['lvl'] += 1

def dbload(name : str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)

def dbsave(db, name : str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)

def setup(bot):
    bot.add_cog(LvlSystem(bot))
