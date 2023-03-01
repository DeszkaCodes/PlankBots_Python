from os import name
import discord
from discord.ext import commands
from scripts.dbhelper import ServerData
from scripts.settings import EmbedSettings
from scripts.helperlib import ErrorEmbed, UnexpectedErrorEmbed, MemberToEmbedAuthor
from scripts.errorlib import UnknownBan, RolePositionTooSmall
import traceback


class Admintools(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        print("Admin Tools System Ready")

    @commands.command(aliases=["töröl", "tisztít", "tisztit", "torol"])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def clear(self, ctx : commands.Context, limit = 10):
        if limit <= 0:
            limit = 1

        successfulDeletes = len(await ctx.channel.purge(limit = limit+1))

        embed=discord.Embed(title="Üzenetek törölve", description=f"Töröltél {successfulDeletes} üzenetet", timestamp=ctx.message.created_at)
        embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
        await ctx.send(content=ctx.author.mention, embed=embed)


    @commands.command(aliases=["kirúg", "kirug", "kidob"])
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx : commands.Context, member : discord.Member, *reasons : str):
        if reasons:
            reason : str = " ".join(reasons)
            reason = reason.capitalize()
        else:
            reasons = None
        
        try:
            await ctx.guild.kick(member, reason=reason)
        except discord.Forbidden as e:
            if e.text == "Missing Permissions":
                raise RolePositionTooSmall(ctx.guild.self_role)
        
        data : ServerData = await ServerData.GetData(ctx.guild)
        
        author = MemberToEmbedAuthor(ctx.author)
        
        embed=discord.Embed(title="Egy tag kickelve lett", timestamp=ctx.message.created_at)
        embed.set_author(name=author["name"], url=author["url"], icon_url=author["icon"])
        embed.add_field(name="Kirúgott tag", value=member.mention, inline=True)
        
        if reason:
            embed.add_field(name="Indok", value=reason, inline=True)
            
        
        if data.trafficChannel:
            channel : discord.TextChannel = ctx.guild.get_channel(data.trafficChannel)
            await channel.send(embed=embed)
        else:
            await ctx.send(embed=embed)
    
    @kick.error
    async def kick_error(self, ctx : commands.Context, error):
        if isinstance(error, RolePositionTooSmall):
            embed = ErrorEmbed(f"A botnak nincs jogosultsága kirúgni a megadott tagot.")
            if not error.role.permissions.kick_members:
                embed.add_field(name="Indok", value="A botnak nincs engedélye kirúgni tagokat.")
            else:
                embed.add_field(name="Indok", value="A kisebb rangú, minta kirúgni kívánt személy.")
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed("Nem létezik ilyen tag a szerveren.")
            embed.add_field(name="Megjelölt tag", value=error.argument)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = ErrorEmbed(f"A botnak nincs jogosultsága kirúgni embereket.")
            embed.add_field(name="Hiányzó rang", value=error.missing_permissions)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = ErrorEmbed(f"Nincs jogosultságod kirúgni embereket.")
            embed.add_field(name="Hiányzó rang", value=error.missing_permissions)
            await ctx.send(content=ctx.author.mention, embed=embed)
        else:
            await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())


    @commands.command(aliases=["tilt", "kitilt", "banhammer"])
    async def ban(self, ctx : commands.Context, member : discord.Member, *reasons : str):
        if reasons:
            reason : str = " ".join(reasons)
            reason = reason.capitalize()
        else:
            reasons = None
        
        try:
            await ctx.guild.ban(member, reason=reason)
        except discord.Forbidden as e:
            if e.text == "Missing Permissions":
                raise RolePositionTooSmall(ctx.guild.self_role)
        
        data : ServerData = await ServerData.GetData(ctx.guild)
        
        author = MemberToEmbedAuthor(ctx.author)
        
        embed=discord.Embed(title="Egy tag ki lett tiltva", timestamp=ctx.message.created_at)
        embed.set_author(name=author["name"], url=author["url"], icon_url=author["icon"])
        embed.add_field(name="Kitiltott tag", value=member.mention, inline=True)
        
        if reason:
            embed.add_field(name="Indok", value=reason, inline=True)
            
        
        if data.trafficChannel:
            channel : discord.TextChannel = ctx.guild.get_channel(data.trafficChannel)
            await channel.send(embed=embed)
        else:
            await ctx.send(embed=embed)
    
    @ban.error
    async def ban_error(self, ctx : commands.Context, error):
        if isinstance(error, RolePositionTooSmall):
            embed = ErrorEmbed(f"A botnak nincs jogosultsága kitiltani a megadott tagot.")
            if not error.role.permissions.ban_members:
                embed.add_field(name="Indok", value="A botnak nincs engedélye kitiltani tagokat.")
            else:
                embed.add_field(name="Indok", value="A kisebb rangú, minta kitiltani kívánt személy.")
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed("Nem létezik ilyen tag a szerveren.")
            embed.add_field(name="Megjelölt tag", value=error.argument)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = ErrorEmbed(f"A botnak nincs jogosultsága kitiltani embereket.")
            embed.add_field(name="Hiányzó rang", value=error.missing_permissions)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = ErrorEmbed(f"Nincs jogosultságod kitiltani embereket.")
            embed.add_field(name="Hiányzó rang", value=error.missing_permissions)
            await ctx.send(content=ctx.author.mention, embed=embed)
        else:
            await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())


    @commands.command(aliases=["felold"])
    async def unban(self, ctx : commands.Context, id : int, *reasons : str):
        if reasons:
            reason : str = " ".join(reasons)
            reason = reason.capitalize()
        else:
            reasons = None
            
        user : discord.User = self.bot.get_user(id)
        
        if not user:
            raise commands.UserNotFound(id)
            
        try:
            await ctx.guild.unban(user, reason=reason)
        except discord.Forbidden as e:
            if e.text == "Missing Permissions":
                raise RolePositionTooSmall(ctx.guild.self_role)
            elif e.text == "Unknown Ban":
                raise UnknownBan(user)
        
        data : ServerData = await ServerData.GetData(ctx.guild)
        
        author = MemberToEmbedAuthor(ctx.author)
        
        embed=discord.Embed(title="Kegyelem", description="Egy tagot feloldottak a kitiltás alól.")
        embed.add_field(name="Feloldott tag", value=user.mention, inline=True)
        embed.add_field(name="Indok", value=reason, inline=True)
        
        if reason:
            embed.add_field(name="Indok", value=reason, inline=True)
            
        
        if data.trafficChannel:
            channel : discord.TextChannel = ctx.guild.get_channel(data.trafficChannel)
            await channel.send(embed=embed)
        else:
            await ctx.send(embed=embed)
            
        
    
    @unban.error
    async def unban_error(self, ctx : commands.Context, error):
        if isinstance(error, RolePositionTooSmall):
            embed = ErrorEmbed(f"A botnak nincs jogosultsága felodani a megadott tagot.")
            if not error.role.permissions.ban_members:
                embed.add_field(name="Indok", value="A botnak nincs engedélye felodani tagokat.")
            else:
                embed.add_field(name="Indok", value="A kisebb rangú, minta felodani kívánt személy.")
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, UnknownBan):
            embed = ErrorEmbed("Ez a Discord felhasználó nincs kitiltva.")
            embed.add_field(name="Felhasználó", value=error.user.mention)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.UserNotFound):
            embed = ErrorEmbed("Ez a Discord felhasználó nem létezik.")
            embed.add_field(name="Megadott azonosító", value=error.argument)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = ErrorEmbed(f"A botnak nincs jogosultsága feloldani embereket.")
            embed.add_field(name="Hiányzó rang", value=error.missing_permissions)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = ErrorEmbed(f"Nincs jogosultságod feloldani embereket.")
            embed.add_field(name="Hiányzó rang", value=error.missing_permissions)
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = ErrorEmbed(f"Az egyik megadott paraméter helytelen.")
            print(error.args)
            if 'Converting to \"int\" failed for parameter \"id\".' in error.args:
                embed.add_field(name="Rossz paraméter", value="A felhasználó azonosítója csak számokból állhat.")
            else:
                embed.add_field(name="Rossz paraméter", value=error.args)
            await ctx.send(content=ctx.author.mention, embed=embed)
        else:
            await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())
    


def setup(bot):
    bot.add_cog(Admintools(bot))