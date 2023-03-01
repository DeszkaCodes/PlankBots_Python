import discord
from discord.ext import commands
import json
from random import randint, choice, random
from asyncio import TimeoutError


class BlackJackSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('BlackJack System Cog Online')

    @commands.command(aliases=['bj', 'BlackJack'])
    @commands.guild_only()
    async def blackjack(self, ctx, bet: str = '5000'):

        

        try:
            user = ctx.author
            server = ctx.guild

            bal = balance(self, user, server.id)

            

            if bet == 'all':
                bet = bal
            else:
                bet = int(bet)

            if bet >= 5000:

                

                if bal >= bet:

                    

                    cards = {
                        'ace': ["<:AS:815590386461442099>", "<:AH:815590386764087327>", "<:AD:815590386357108747>",
                                "<:AC:815590386637602816>"],
                        '10': ["<:QS:815590387031736370>", "<:QH:815590386881265684>", "<:QD:815590386897518593>",
                               "<:QC:815590387032784937>", "<:KS:815590387049431050>", "<:KH:815590386784927746>",
                               "<:KD:815590386838798346>", "<:KC:815590386931990559>", "<:JS:815590386466422797>",
                               "<:JH:815590386629869578>", "<:JD:815590386642452522>", "<:JC:815590386310447105>"],
                        '3': ["<:3S:815590385412866048>", "<:3H:815590385341825054>", "<:3D:815590385383768104>",
                              "<:3C:815590385359388682>"],
                        '4': ["<:4S:815590385765449738>", "<:4H:815590385451663390>", "<:4D:815590385509203998>",
                              "<:4C:815590385488756756>"],
                        '5': ["<:5S:815590385836621834>", "<:5H:815590385718919228>", "<:5D:815590385723375658>",
                              "<:5C:815590385430691851>"],
                        '6': ["<:6S:815590385816174635>", "<:6H:815590385598332929>", "<:6D:815590385920376842>",
                              "<:6C:815590385770037288>"],
                        '7': ["<:7S:815590386163777559>", "<:7H:815590385802805269>", "<:7D:815590386428411914>",
                              "<:7C:815590386012782614>"],
                        '8': ["<:8S:815590386240061452>", "<:8H:815590386688851978>", "<:8D:815590386583863337>",
                              "<:8C:815590386705629214>"],
                        '9': ["<:9S:815590386612568064>", "<:9H:815590386755436604>", "<:9D:815590386361827369>",
                              "<:9C:815590386537463808>"],
                    }

                    embed = discord.Embed(
                        title='BlackJack játszma',
                        description='Parancsok: `hit` `double down` `stand`',
                        color=0xC99B00
                    )

                    embed.set_author(
                        name=ctx.author,
                        url=f'https://discord.com/users/{ctx.author.id}',
                        icon_url=ctx.author.avatar_url
                    )

                    you = [
                        '', 0
                    ]

                    dealer = [
                        '', 0
                    ]

                    latszat = [
                        '', 0
                    ]

                    def add(userTest, opponent, lowRange=3, highRange=11):

                        num = randint(lowRange, highRange)
                        cardChoice = ''

                        if userTest:
                            cardChoice += you.pop(0)

                        else:
                            cardChoice += dealer.pop(0)

                        if num == 11:
                            cardChoice += '{} '.format(choice(tuple(cards['ace'])))
                            if num + opponent[0] > 21:
                                num = 1
                        else:
                            cardChoice += '{} '.format(choice(tuple(cards[str(num)])))

                        if userTest:
                            num += you.pop()

                            you.append(cardChoice)
                            you.append(num)

                        else:
                            num += dealer.pop()

                            dealer.append(cardChoice)
                            dealer.append(num)


                    def check(m):
                        if m.content.lower() == 'hit' and m.author == ctx.author:
                            return 'hit'
                        elif m.content.lower() == 'double down' and m.author == ctx.author:
                            return 'dd'
                        elif m.content.lower() == 'stand' and m.author == ctx.author:
                            return 'stand'

                    # START ADDING
                    add(False, dealer)

                    latszat = [
                        str(dealer.copy().pop(0)) + "<:back:816081054519001128>", dealer.copy().pop(1)
                    ]

                    add(False, dealer)

                    add(True, you)
                    add(True, you)


                    embed.add_field(
                        name='Te kártyáid\n'
                             '{}'.format(you[0]),
                        value='Összeg: {}'.format(you[1])
                    )

                    embed.add_field(
                        name='Osztói kártyái\n'
                             '{}'.format(latszat[0]),
                        value='Összeg: {}'.format(latszat[1])
                    )

                    embed.add_field(
                        name='Tét',
                        value='{:,} <:plancoin:799180662166781992>'.format(int(bet)),
                        inline=False
                    )

                    #RNG TWEEK AT THE MOMEN 40% WINRATE

                    msg = await ctx.send(ctx.author.mention, embed=embed)

                    end = False

                    instaWin = True

                    while not end and you[1] < 21 and dealer[1] < 21:

                        instaWin = False

                        cont = await self.bot.wait_for('message', check=check, timeout=15)

                        cont = cont.content

                        if cont == 'hit':

                            add(True, you)

                            if random() >= 0.5 and dealer[1] < 16:
                                add(False, dealer)
                            elif random() > 0.80:
                                add(False, dealer)

                            embed.set_field_at(
                                index=0,
                                name='Te kártyáid\n'
                                     '{}'.format(you[0]),
                                value='Összeg: {}'.format(you[1])
                            )

                            await msg.edit(embed=embed)

                        elif cont == 'stand':
                            if dealer[1] < 10:
                                add(False, dealer)
                            elif dealer[1] < 17:
                                add(False, dealer, 3, 5)

                            end = True

                        elif cont == 'dd' or cont == 'double down':
                            end = True

                            if dealer[1] < 12:
                                add(False, dealer)
                            elif dealer[1] < 17:
                                add(False, dealer, 3, 5)

                            bet *= 2

                            bet = int(bet)

                            add(True, you)

                            embed.set_field_at(
                                index=0,
                                name='Te kártyáid\n'
                                     '{}'.format(you[0]),
                                value='Összeg: {}'.format(you[1])
                            )

                            embed.set_field_at(
                                index=2,
                                name='Tét',
                                value='{:,} <:plancoin:799180662166781992>'.format(int(bet)),
                                inline=False
                            )

                            await msg.edit(embed=embed)

                    embed.set_field_at(
                        index=1,
                        name='Osztói kártyái\n'
                             '{}'.format(dealer[0]),
                        value='Összeg: {}'.format(dealer[1])
                    )


                    windb = dbload('blackjackatlag')


                    if (dealer[1] > 21 and you[1] <= 21) or dealer[1] < you[1] <= 21:

                        windb.append(1)

                        if instaWin:
                            moneyChange(
                                self,
                                ctx.author,
                                ctx.guild.id,
                                int(bet * 2.5)
                            )
                        else:
                            moneyChange(
                                self,
                                ctx.author,
                                ctx.guild.id,
                                int(bet) * 2
                            )

                        embed = discord.Embed(
                            title='BlackJack játszma',
                            color=0x00b000
                        )

                        embed.set_author(
                            name=ctx.author,
                            url=f'https://discord.com/users/{ctx.author.id}',
                            icon_url=ctx.author.avatar_url
                        )

                        if instaWin:
                            embed.add_field(
                                name='Nyertél!',
                                value='{:,} <:plancoin:799180662166781992>'.format(int(bet * 1.5)),
                                inline=False
                            )
                        else:
                            embed.add_field(
                                name='Nyertél!',
                                value='{:,} <:plancoin:799180662166781992>'.format(int(bet)),
                                inline=False
                            )

                        embed.add_field(
                            name='Te kártyáid\n'
                                 '{}'.format(you[0]),
                            value='Összeg: {}'.format(you[1])
                        )

                        embed.add_field(
                            name='Osztói kártyái\n'
                                 '{}'.format(dealer[0]),
                            value='Összeg: {}'.format(dealer[1])
                        )

                    elif (you[1] == dealer[1]) and you[1] <= 21:

                        windb.append(0)

                        moneyChange(
                            self,
                            ctx.author,
                            ctx.guild.id,
                            int(bet)
                        )

                        embed = discord.Embed(
                            title='BlackJack játszma',
                            color=0x8a7c74
                        )

                        embed.set_author(
                            name=ctx.author,
                            url=f'https://discord.com/users/{ctx.author.id}',
                            icon_url=ctx.author.avatar_url
                        )

                        embed.add_field(
                            name='Döntetlen',
                            value='Vissza kaptad a tétet.'.format(int(bet)),
                            inline=False
                        )

                        embed.add_field(
                            name='Te kártyáid\n'
                                 '{}'.format(you[0]),
                            value='Összeg: {}'.format(you[1])
                        )

                        embed.add_field(
                            name='Osztói kártyái\n'
                                 '{}'.format(dealer[0]),
                            value='Összeg: {}'.format(dealer[1])
                        )

                    else:

                        windb.append(0)

                        embed = discord.Embed(
                            title='BlackJack játszma',
                            color=0xb80000
                        )

                        embed.set_author(
                            name=ctx.author,
                            url=f'https://discord.com/users/{ctx.author.id}',
                            icon_url=ctx.author.avatar_url
                        )

                        embed.add_field(
                            name='Vesztettél!',
                            value='{:,} <:plancoin:799180662166781992>'.format(int(bet)),
                            inline=False
                        )

                        embed.add_field(
                            name='Te kártyáid\n'
                                 '{}'.format(you[0]),
                            value='Összeg: {}'.format(you[1])
                        )

                        embed.add_field(
                            name='Osztói kártyái\n'
                                 '{}'.format(dealer[0]),
                            value='Összeg: {}'.format(dealer[1])
                        )

                    moneyChange(
                        self,
                        ctx.author,
                        ctx.guild.id,
                        -int(bet)
                    )

                    await msg.edit(embed=embed)

                    dbsave(windb, 'blackjackatlag')

                else:
                    embed = newErr('Nincs ennyi pénzed.')
                    await ctx.send(ctx.author.mention, embed=embed)

            else:
                embed = newErr('A belépő tét 5000 <:plancoin:799180662166781992>')
                await ctx.send(ctx.author.mention, embed=embed)
        except ValueError:
            embed = newErr('Helytelen paraméterek')

            embed.add_field(
                name='Helytelen paraméter',
                value=bet,
                inline=False
            )

            embed.add_field(
                name='Helyes parancs',
                value='`!pb blackjack <tét szám/all>`',
                inline=False
            )
            await ctx.send(user.mention, embed=embed)

        except TimeoutError:
            embed = newErr('Játék lemondva')

            windb = dbload('blackjackatlag')

            if (dealer[1] > 21 and you[1] <= 21) or dealer[1] < you[1] <= 21:

                windb.append(1)

                if instaWin:
                    moneyChange(
                        self,
                        ctx.author,
                        ctx.guild.id,
                        int(bet * 2.5)
                    )
                else:
                    moneyChange(
                        self,
                        ctx.author,
                        ctx.guild.id,
                        int(bet) * 2
                    )

                if instaWin:
                    embed.add_field(
                        name='Nyertél!',
                        value='{:,} <:plancoin:799180662166781992>'.format(int(bet * 1.5)),
                        inline=False
                    )
                else:
                    embed.add_field(
                        name='Nyertél!',
                        value='{:,} <:plancoin:799180662166781992>'.format(int(bet)),
                        inline=False
                    )

                embed.add_field(
                    name='Te kártyáid\n'
                         '{}'.format(you[0]),
                    value='Összeg: {}'.format(you[1])
                )

                embed.add_field(
                    name='Osztói kártyái\n'
                         '{}'.format(dealer[0]),
                    value='Összeg: {}'.format(dealer[1])
                )

            elif (you[1] == dealer[1]) and you[1] <= 21:

                windb.append(0)

                moneyChange(
                    self,
                    ctx.author,
                    ctx.guild.id,
                    int(bet)
                )

                embed.add_field(
                    name='Döntetlen',
                    value='Vissza kaptad a tétet.'.format(int(bet)),
                    inline=False
                )

                embed.add_field(
                    name='Te kártyáid\n'
                         '{}'.format(you[0]),
                    value='Összeg: {}'.format(you[1])
                )

                embed.add_field(
                    name='Osztói kártyái\n'
                         '{}'.format(dealer[0]),
                    value='Összeg: {}'.format(dealer[1])
                )

            else:

                windb.append(0)

                embed.add_field(
                    name='Vesztettél!',
                    value='{:,} <:plancoin:799180662166781992>'.format(int(bet)),
                    inline=False
                )

                embed.add_field(
                    name='Te kártyáid\n'
                         '{}'.format(you[0]),
                    value='Összeg: {}'.format(you[1])
                )

                embed.add_field(
                    name='Osztói kártyái\n'
                         '{}'.format(dealer[0]),
                    value='Összeg: {}'.format(dealer[1])
                )

            moneyChange(
                self,
                ctx.author,
                ctx.guild.id,
                -int(bet)
            )

            dbsave(windb, 'blackjackatlag')

            embed.add_field(
                name='Indok',
                value='Letelt a döntési idő.',
                inline=False
            )
            await ctx.send(ctx.author.mention, embed=embed)


# 0xC99B00
# <:plancoin:799180662166781992>

def dbload(name: str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)


def dbsave(db, name: str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)


def moneyChange(self, user: discord.User, server, amount):
    users = dbload('users')

    users[f'{server}'][f'{user.id}']['bal'] += amount

    dbsave(users, 'users')


def newErr(reason: str):
    embed = discord.Embed(title='Hiba', description=reason, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed


def balance(self, user: discord.User, server):
    users = dbload('users')
    return users[f'{server}'][f'{user.id}']['bal']


def setup(bot):
    bot.add_cog(BlackJackSystem(bot))