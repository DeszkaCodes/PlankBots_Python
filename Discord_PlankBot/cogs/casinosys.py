import discord
from discord.ext import commands
from random import randint
import json


class Casinoystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    timetable = {'minute': 60, 'hour': 3600, 'day': 86400, 'week': 604800,
                 'month': 2592000}

    @commands.Cog.listener()
    async def on_ready(self):
        print('Casino System Cog Online')

    # SZERENCSEJÁTÉK-----------------------------------------------------------------

    @commands.group(aliases=['lottó'], invoke_without_command=True)
    @commands.guild_only()
    @commands.cooldown(1, 1.5 * timetable['hour'], commands.BucketType.member)
    async def lotto(self, ctx,):

        szelveny = 2
        szelvenyAr = 5000
        kiadas = szelvenyAr * szelveny

        if balance(self, ctx.author, ctx.guild.id) >= kiadas:

            moneyChange(self, ctx.author, ctx.guild.id, -kiadas)

            prize = {}
            prize['főnyeremény'] = {}
            prize['főnyeremény']['esély'] = 2
            prize['főnyeremény']['max'] = 20000000
            prize['főnyeremény']['min'] = 5000000
            prize['főnyeremény']['round'] = 1000000
            prize['nagynyeremény'] = {}
            prize['nagynyeremény']['esély'] = 50
            prize['nagynyeremény']['max'] = 5000000
            prize['nagynyeremény']['min'] = 1000000
            prize['nagynyeremény']['round'] = 100000
            prize['közepesnyeremény'] = {}
            prize['közepesnyeremény']['esély'] = 125
            prize['közepesnyeremény']['max'] = 250000
            prize['közepesnyeremény']['min'] = 10000
            prize['közepesnyeremény']['round'] = 10000
            prize['kisnyeremény'] = {}
            prize['kisnyeremény']['esély'] = 800
            prize['kisnyeremény']['max'] = 50000
            prize['kisnyeremény']['min'] = 10000
            prize['kisnyeremény']['round'] = 1000

            payment = 0

            embed = discord.Embed(
                title='Lottó eredmények',
                description='{} lottó eredményei.'.format(ctx.author.name),
                color=0xC99B00
            )
            embed.set_author(
                name=ctx.author,
                url=f'https://discord.com/users/{ctx.author.id}',
                icon_url=ctx.author.avatar_url
            )

            embed.set_footer(
                text='Csak 1x lottózhatsz másfél óránként.'
            )

            for i in range(szelveny):
                rng = randint(0, 1000)

                rngPayment = 0

                if rng <= prize['főnyeremény']['esély']:
                    rngPayment = rounder(
                        randint(prize['főnyeremény']['min'], prize['főnyeremény']['max']),
                        prize['főnyeremény']['round']
                    )

                    embed.add_field(
                        name='{}. szelvény: FŐNYEREMÉNY!'.format(i + 1),
                        value='{:,} <:plancoin:799180662166781992>'.format(rngPayment),
                        inline=False
                    )

                    toplist = dbload('lottowinners')
                    cards = dbload('globalusers')

                    if ctx.author.id not in toplist:
                        if len(toplist) == 10:
                            print(len(toplist))
                            exuser = self.bot.get_user(toplist.pop(0))
                            del cards[str(exuser.id)]["1024"]

                            toplist.append(ctx.author.id)
                            if str(ctx.author.id) not in cards:
                                cards[str(ctx.author.id)] = {}

                            cards[str(ctx.author.id)]["1024"] = {}
                            cards[str(ctx.author.id)]["1024"]['name'] = 'Lottó nyertes'
                            cards[str(ctx.author.id)]["1024"]['desc'] = 'Megnyerte a FŐNYEREMÉNY-t.'

                        else:
                            toplist.append(ctx.author.id)
                            if str(ctx.author.id) not in cards:
                                cards[str(ctx.author.id)] = {}

                            cards[str(ctx.author.id)]["1024"] = {}
                            cards[str(ctx.author.id)]["1024"]['name'] = 'Lottó nyertes'
                            cards[str(ctx.author.id)]["1024"]['desc'] = 'Megnyerte a FŐNYEREMÉNY-t.'

                    dbsave(toplist, 'lottowinners')
                    dbsave(cards, 'globalusers')

                elif rng <= prize['nagynyeremény']['esély']:
                    rngPayment = rounder(
                        randint(prize['nagynyeremény']['min'], prize['nagynyeremény']['max']),
                        prize['nagynyeremény']['round']
                    )

                    embed.add_field(
                        name='{}. szelvény: NYERT'.format(i + 1),
                        value='{:,} <:plancoin:799180662166781992>'.format(rngPayment),
                        inline=False
                    )

                elif rng <= prize['közepesnyeremény']['esély']:
                    rngPayment = rounder(
                        randint(prize['közepesnyeremény']['min'], prize['közepesnyeremény']['max']),
                        prize['közepesnyeremény']['round']
                    )

                    embed.add_field(
                        name='{}. szelvény: NYERT'.format(i + 1),
                        value='{:,} <:plancoin:799180662166781992>'.format(rngPayment),
                        inline=False
                    )

                elif rng <= prize['kisnyeremény']['esély']:
                    rngPayment = rounder(
                        randint(prize['kisnyeremény']['min'], prize['kisnyeremény']['max']),
                        prize['kisnyeremény']['round']
                    )

                    embed.add_field(
                        name='{}. szelvény: NYERT'.format(i + 1),
                        value='{:,} <:plancoin:799180662166781992>'.format(rngPayment),
                        inline=False
                    )

                else:
                    embed.add_field(
                        name='{}. szelvény: VESZTETT'.format(i + 1),
                        value='{:,} <:plancoin:799180662166781992>'.format(rngPayment),
                        inline=False
                    )

                payment += rngPayment

            if payment >= 10000000:
                embed.set_thumbnail(
                    url='https://imgur.com/uN0HXur.png'
                )
            elif payment > 1000000:
                embed.set_thumbnail(
                    url='https://imgur.com/aFJ5GQB.png'
                )
            elif payment > 100000:
                embed.set_thumbnail(
                    url='https://imgur.com/sWJy2V8.png'
                )
            elif payment >= kiadas:
                embed.set_thumbnail(
                    url='https://imgur.com/S8BQtYz.png'
                )
            else:
                embed.set_thumbnail(
                    url='https://imgur.com/Lqltz9R.png'
                )

            embed.add_field(
                name='Végösszeg',
                value='{:,} <:plancoin:799180662166781992>'.format(payment),
                inline=False
            )

            moneyChange(self, ctx.author, ctx.guild.id, payment)

            await ctx.send(ctx.author.mention, embed=embed)

        else:
            ctx.command.reset_cooldown(ctx)
            embed = newErr('Nincs elég pénzed {} szelvényre.'.format(szelveny))
            await ctx.send(ctx.author.mention, embed=embed)

    @lotto.command(aliases=['toplista'])
    async def toplist(self, ctx):

        list = dbload('lottowinners')

        embed=discord.Embed(
            title='Lottó főnyertesek',
            description='Az utolsó 10 ember aki FŐNYEREMÉNY-t nyert a lottón.',
            color=0xC99B00
        )

        embed.set_thumbnail(
            url='https://imgur.com/uN0HXur.png'
        )

        embed.add_field(
            name='** **',
            value='** **',
            inline=False
        )

        if len(list) != 0:
            for i in list:
                user = self.bot.get_user(i)
                embed.add_field(
                    name='{}'.format(user.name),
                    value='** **',
                    inline=False
                )
        else:
            embed.add_field(
                name='Még nincs 1 nyertes sem.',
                value='** **',
                inline=False
            )

        await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['Roulette', 'rulett', 'Rulett'])
    @commands.guild_only()
    async def roulette(self, ctx, choice: str, betStr: str):

        try:
            if betStr == 'all':
                bet = balance(self, ctx.author, ctx.guild.id)
            else:
                bet = int(betStr)

            if bet >= 5000:
                if bet <= balance(self, ctx.author, ctx.guild.id):
                    moneyChange(self, ctx.author, ctx.guild.id, -(bet))
                    emojis = ("<:00:796395538652201030>", "<:01:796395538491768884>", "<:02:796395538371051531>",
                              "<:03:796395538412863560>", "<:04:796395538470666241>", "<:05:796395538722324545>",
                              "<:06:796395538676842527>", "<:07:796395538991022210>", "<:08:796395539066781727>",
                              "<:09:796395539045941298>", "<:10:796395539159580712>", "<:11:796395539121832016>",
                              "<:12:796395539142803518>", "<:13:796395539490930747>", "<:14:796395539486212096>",
                              "<:15:796395539498795018>", "<:16:796395539981402152>", "<:17:796395539767885824>",
                              "<:18:796395539985989682>", "<:19:796395539993853962>", "<:20:796395540031733791>",
                              "<:21:796395540219953152>", "<:22:796395540006830080>", "<:23:796395540291518495>",
                              "<:24:796395539855966229>", "<:25:796395540174733342>", "<:26:796395539846398003>",
                              "<:27:796395540320747570>", "<:28:796395540258226187>", "<:29:796395540165689344>",
                              "<:30:796395540216676402>", "<:31:796395540127416330>", "<:32:796395540228079626>",
                              "<:33:796395540258357290>", "<:34:796395540257439744>", "<:35:796395539989397515>",
                              "<:36:796395540316684329>")
                    winNum = randint(0, 36)
                    didWin = False
                    input = True
                    embed = discord.Embed(title="Roulette eredmény",
                                          description="A pörgetett szám:   {} ({})".format(emojis[winNum], winNum),
                                          color=0xC99B00)
                    embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                                     icon_url=ctx.author.avatar_url)
                    if choice.isnumeric():
                        if choice == str(winNum):
                            bet = bet * 36
                            didWin = True
                    elif choice.lower() == "páros" or choice.lower() == "even":
                        if winNum % 2 == 0:
                            bet += bet
                            didWin = True
                    elif choice.lower() == "páratlan" or choice.lower() == "odd":
                        if winNum % 2 != 0:
                            bet += bet
                            didWin = True
                    elif choice.lower() == "piros" or choice.lower() == "red":
                        reds = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)
                        if winNum in reds:
                            bet += bet
                            didWin = True
                    elif choice.lower() == "fekete" or choice.lower() == "black":
                        blacks = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35)
                        if winNum in blacks:
                            bet += bet
                            didWin = True
                    elif choice == "1/12":
                        onethird = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
                        if winNum in onethird:
                            bet += bet * 2
                            didWin = True
                    elif choice == "2/12":
                        twothird = (13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24)
                        if winNum in twothird:
                            bet += bet * 2
                            didWin = True
                    elif choice == "3/12":
                        threethird = (25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36)
                        if winNum in threethird:
                            bet += bet * 2
                            didWin = True
                    else:
                        input = False
                        embed = newErr('Erre nem fogadhatsz. ({})'.format(choice))

                    if input:
                        if didWin:
                            embed.set_thumbnail(url='https://imgur.com/aFJ5GQB.png')
                            embed.add_field(name="Nyertél!", value="Hurrá!", inline=True)
                            embed.add_field(name="Nyereményed: ",
                                            value="{:,} <:plancoin:799180662166781992>".format(bet),
                                            inline=False)
                            moneyChange(self, ctx.author, ctx.guild.id, bet)
                        else:
                            embed.set_thumbnail(url='https://imgur.com/Lqltz9R.png')
                            embed.add_field(name="Vesztettél!", value=":(", inline=True)
                            embed.add_field(name="Elbuktál:", value="{:,} <:plancoin:799180662166781992>".format(bet),
                                            inline=False)

                else:
                    embed = newErr('Nincs ennyi pénz a számládon.')

            else:
                embed = newErr('A belépő tét legalább 5,000 <:plancoin:799180662166781992>')

        except ValueError:
            embed = newErr('Helytelen paraméterek.')
            embed.add_field(
                name='Helyes használat',
                value='`!pb roulette <fogadás> <tét>`',
                inline=False
            )

        finally:

            await ctx.send(ctx.author.mention, embed=embed)

    @roulette.error
    async def roulette_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = newErr('Nem adtál meg fogadást vagy tétet.')

            embed.add_field(
                name='Helyes parancs',
                value='`!pb roulette <fogadás> <tét>`'
            )

            embed.add_field(
                name='Fogadások',
                value='-számok\n'
                      '-páros vagy even\n'
                      '-páratlan vagy odd\n'
                      '-piros vagy red\n'
                      '-fekete vagy black\n'
                      '1/12\n'
                      '2/12\n'
                      '3/12',
                inline=False
            )

            await ctx.send(embed=embed)

    @commands.command(aliases=['slot machine', 'slot_machine', 'szerencsejatek', 'szerencsejáték'])
    @commands.guild_only()
    async def slotmachine(self, ctx):
        if balance(self, ctx.author, ctx.guild.id) >= 500:
            moneyChange(self, ctx.author, ctx.guild.id, -500)
            imgs = ('<:bar:797975602971541525>', '<:apple:797975602904825876>', '<:banana:797975602753830913>',
                    '<:cherry:797975603113361448>', '<:grape:797975602824740865>', '<:lime:797975603055558726>',
                    '<:melon:797975603092914216>', '<:peach:797975603118080010>')
            choices = (randint(0, 7), randint(0, 7), randint(0, 7))
            embed = discord.Embed(title="Játékautómata", description="", color=0xC99B00)
            embed.set_author(name=ctx.author, url=f'https://discord.com/users/{ctx.author.id}',
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name="Kapott szimbólumok:",
                            value="{} {} {}".format(imgs[choices[0]], imgs[choices[1]], imgs[choices[2]]), inline=True)
            if choices[0] == choices[1] and choices[0] == choices[2]:
                win = rounder(randint(75000, 100000), 1000)
                embed.set_thumbnail(url='https://imgur.com/aFJ5GQB.png')
                embed.add_field(name='Siker!', value='Nyertél {:,} <:plancoin:799180662166781992>-t.'.format(win),
                                inline=False)
                moneyChange(self, ctx.author, ctx.guild.id, win)
                await ctx.send(embed=embed)
            elif choices[0] == choices[1] or choices[1] == choices[2]:
                win = rounder(randint(10000, 50000), 1000)
                embed.set_thumbnail(url='https://imgur.com/S8BQtYz.png')
                embed.add_field(name='Félsiker!', value='Nyertél {:,} <:plancoin:799180662166781992>-t.'.format(win),
                                inline=False)
                moneyChange(self, ctx.author, ctx.guild.id, win)
                await ctx.send(embed=embed)
            else:
                embed.set_thumbnail(url='https://imgur.com/Lqltz9R.png')
                embed.add_field(name='Balszerencse!', value='Nem nyertél semmit.', inline=False)
                await ctx.send(embed=embed)


        else:
            ctx.command.reset_cooldown(ctx)
            embed = newErr('Nincs elég pénzed.')
            await ctx.send(embed=embed)


def dbload(name: str):
    with open('db/{}.json'.format(name), 'r') as f:
        return json.load(f)


def dbsave(db, name: str):
    with open('db/{}.json'.format(name), 'w') as f:
        json.dump(db, f)


def rounder(num, amount):
    num = int(num / amount) * amount
    return num


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
    bot.add_cog(Casinoystem(bot))
