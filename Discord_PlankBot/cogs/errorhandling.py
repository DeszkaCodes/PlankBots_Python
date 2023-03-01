import discord
from discord.ext import commands
from termcolor import colored
import datetime


class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Error Handling Cog Online')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        date = datetime.datetime.now()
        if isinstance(error, commands.errors.CommandNotFound):
            embed = newErr('Nem létezik ilyen parancs.')
            embed.add_field(
                name='Nem ismered még a parancsokat?\nÍrd be:',
                value='`!pb help`',
                inline=False
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.CommandOnCooldown):

            ido = int(error.retry_after)
            maradt = ''
            maradek = 0

            embed = newErr('Még nem használhatod ezt a parancsot.')
            
            if int(ido / 86400) > 0:
                napok = int(ido / 86400)
                maradt+= '{} nap '.format(napok)
                ido -= napok * 86400


            if int(ido / 3600) > 0:
                orak = int(ido / 3600)
                maradt += ' {} óra '.format(orak)
                ido -= orak * 3600


            if int(ido / 60) > 0:
                percek = int(ido / 60)
                maradt += '{} perc '.format(percek)
                ido -= percek * 60

            maradt += '{} másodperc múlva.'.format(ido)


            embed.add_field(
                name='Próbáld újra',
                value=maradt
            )

            await ctx.send(embed=embed)

        elif isinstance(error, commands.errors.MissingRequiredArgument):
            print(
                colored('\n{}\nMissingRequiredArgument ERROR\nNew error: {}\nMessage: {}\nAuthor: {}\nServer: {}', 'red').format(
                    date.strftime('%H:%M:%S'), error,
                    ctx.author, ctx.message.content, ctx.guild.name))

        elif isinstance(error, commands.errors.UserNotFound):
            print(
                colored('\n{}\nUserNotFound ERROR\nNew error: {}\nMessage: {}\nAuthor: {}\nServer: {}', 'red').format(
                    date.strftime('%H:%M:%S'), error,
                    ctx.author, ctx.message.content, ctx.guild.name))

        elif isinstance(error, commands.errors.MemberNotFound):
            print(
                colored('\n{}\nMemberNotFound ERROR\nNew error: {}\nMessage: {}\nAuthor: {}\nServer: {}', 'red').format(
                    date.strftime('%H:%M:%S'), error,
                    ctx.author, ctx.message.content, ctx.guild.name))

        elif isinstance(error, commands.errors.RoleNotFound):
            embed = newErr('Nem létezik ilyen rang a szerveren.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.ChannelNotFound):
            embed = newErr('Nem létezik ilyen szoba a szerverben.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.NoPrivateMessage):
            embed = newErr('Ezt az üzenetet csak szerverekben lehet használni.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = newErr('Nincs rangod ezt végrehajtani.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.BotMissingPermissions):
            embed = newErr('A bot nem rendelkezik elég magas ranggal.')
            embed.add_field(
                name='Megoldások',
                value=
                '-a bot legyen magasabb rangú, mint az adandó role\n'
                '-a botnak legyen Administrator engedélye',
                inline=False
            )

        elif isinstance(error, discord.Forbidden):
            embed = newErr('Ez a parancs le van tiltva')
            embed.add_field(
                name='Lehetséges okok',
                value='-ki van kapcsolva, hogy üzeneteket küldhessenek a szerverről'
            )

        elif isinstance(error, commands.errors.CommandInvokeError):
            print(colored('\n{}\nNew error: {}\nCtx: {}', 'red').format(date.strftime('%H:%M:%S'), error, ctx))
            embed = newErr('Egy hibába ütköztünk.')
            embed.add_field(name="Részletek:", value='**{}**'.format(error.original))
            await ctx.send(embed=embed)
        else:
            print(
                colored('\n{}\nUNHANDLED ERROR\nNew error: {}\nMessage: {}\nAuthor: {}\nServer: {}', 'red').format(date.strftime('%H:%M:%S'), error,
                                                                                       ctx.author, ctx.message.content, ctx.guild.name))


def newErr(desc: str):
    embed = discord.Embed(title='Hiba', description=desc, color=0xff0000)
    embed.set_thumbnail(url='https://imgur.com/CAc2Sar.png')
    return embed


def setup(bot):
    bot.add_cog(ErrorHandling(bot))