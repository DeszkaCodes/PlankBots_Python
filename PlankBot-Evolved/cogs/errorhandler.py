import traceback
import discord
from discord.ext import commands
from scripts.errorlib import BotUserMentioned, UnhandledException  
from scripts.helperlib import ErrorEmbed, UnexpectedErrorEmbed


class Errorhandler(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        print("Error Handler System Ready")

    @commands.Cog.listener()
    async def on_command_error(self, ctx : commands.Context, error):

        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        error = getattr(error, 'original', error)


        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed("A megadott tag nem létezik.")
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.UserNotFound):
            embed = ErrorEmbed("Nem létezik ilyen Discord felhasználó.")
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, BotUserMentioned):
            embed = ErrorEmbed(f"A megjelölt tag egy bot felhasználó.")
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = ErrorEmbed(f"Nem rendelkezel a(z) {error.missing_permissions} ranggal, ami kötelező ehhez a parancshoz.")
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = ErrorEmbed(f"A bot nem rendelkezik ehhez a parancshoz való ranggal. ({error.missing_permissions})")
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            embed = ErrorEmbed(f"Nem létezik ilyen parancs.")
            await ctx.send(content=ctx.author.mention, embed=embed)
        else:
            await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())
        

def setup(bot):
    bot.add_cog(Errorhandler(bot))
