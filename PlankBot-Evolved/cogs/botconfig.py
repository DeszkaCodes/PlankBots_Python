import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from data.database import db
from scripts.helperlib import EmbedSettings, ErrorEmbed, UnexpectedErrorEmbed
import traceback


class Botconfig(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        print("Bot Config System Ready")

    
    @commands.command(aliases=["üdvözlő", "üdvözlő szoba", "udvozlo szoba"])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def udvozlo(self, ctx : commands.Context, channel : discord.TextChannel):
        db.execcommit("UPDATE ServerData SET TrafficChannel = ? WHERE ID = ?", channel.id, ctx.guild.id)

        embed=discord.Embed(title="Üdvözlő szoba sikeresen beállítva", description="Sikeresen beállítottad az üdvözlő szobát.", color=EmbedSettings.successColor())
        embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
        embed.add_field(name="Szoba", value=channel.mention, inline=False)
        embed.set_footer(text="Ha nem jelennek meg az üzenetek a szoba törölve lett, vagy megváltozott az azonosítója.")
        
        await ctx.send(content=ctx.author.mention, embed=embed)

    @udvozlo.error
    async def udvozlo_error(self, ctx : commands.Context, error):
        if isinstance(error, MissingRequiredArgument):
            embed = ErrorEmbed(f"Nem adtad meg a {error.param} paraméterét a parancsnak.")
            await ctx.send(content=ctx.author.mention, embed=embed)
        else:
            await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())

        
    @commands.command(aliases=["szint szoba"])
    @commands.guild_only()
    async def szintszoba(self, ctx : commands.Context, channel : discord.TextChannel):
        db.execcommit("UPDATE ServerData SET LVLChannel = ? WHERE ID = ?", channel.id, ctx.guild.id)

        embed=discord.Embed(
                title="Szintlépés értesítő szoba sikeresen beállítva",
                description="Sikeresen beállítottad az üdvözlő szobát.",
                color=EmbedSettings.successColor()
            )

        embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
        embed.add_field(name="Szoba", value=channel.mention, inline=False)
        embed.set_footer(text="Ha nem jelennek meg az üzenetek a szoba törölve lett, vagy megváltozott az azonosítója.")
        
        await ctx.send(content=ctx.author.mention, embed=embed)

    @szintszoba.error
    async def szintszoba_error(self, ctx : commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = ErrorEmbed(f"Nem adtad meg a {error.param} paraméterét a parancsnak.")
            await ctx.send(content=ctx.author.mention, embed=embed)
        else:
            await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())



def setup(bot):
    bot.add_cog(Botconfig(bot))
