from datetime import datetime
import discord
from discord.ext import commands
from scripts.dbhelper import LocalData, ServerData
from data.database import db


class Traffichandle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Traffic Handler System Ready")

    @commands.Cog.listener()
    async def on_member_join(self, member : discord.Member):
        if not member.bot:
            await LocalData.GetData(member)

        data : ServerData = await ServerData.GetData(member.guild)

        channelId : int = data.trafficChannel

        if channelId:
            channel : discord.TextChannel = member.guild.get_channel(channelId)
            if channel:
                await channel.send(f"{member.mention} csatlakozott a szerverhez, hurrá!")


    @commands.Cog.listener()
    async def on_member_remove(self, member : discord.Member):
        await LocalData.DeleteUser(member)
        
        data : ServerData = await ServerData.GetData(member.guild)

        channelId : int = data.trafficChannel
        if channelId:
            channel : discord.TextChannel = member.guild.get_channel(channelId)
            if channel:
                await channel.send(f"{member.mention} távozott közülünk.")


    @commands.Cog.listener()
    async def on_member_ban(self, guild : discord.Guild, user : discord.User):
        data : ServerData = await ServerData.GetData(guild)

        channelId : int = data.trafficChannel

        if channelId:
            channel : discord.TextChannel = guild.get_channel(channelId)
            if channel:
                embed=discord.Embed(
                        title="Lecsapott a ban hammer",
                        description="Egy szerencsétlen tagot utolért a ban kalapács haragja.",
                        timestamp=datetime.now()
                    )
                embed.add_field(name="Áldozat", value=user.mention, inline=False)
                await channel.send(embed=embed)
        
        
    @commands.Cog.listener()
    async def on_member_unban(self, guild : discord.Guild, user : discord.User):
        data : ServerData = await ServerData.GetData(guild)

        channelId : int = data.trafficChannel

        if channelId:
            channel : discord.TextChannel = guild.get_channel(channelId)
            if channel:
                embed=discord.Embed(
                        title="Megenyhült a büntetés",
                        description=f"{user.mention} örömére fel lett oldva a ban.",
                        timestamp=datetime.now()
                    )
                await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_join(self, guild : discord.Guild):
        db.execcommit("INSERT OR IGNORE INTO ServerData (ID) VALUES (?)", guild.id)
        # TODO: send the owner a message about the configuration of the bot

    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild : discord.Guild):
        db.execcommit("DELETE FROM ServerData WHERE ID = ?", guild.id)

        # TODO: send the owner a message about the removement of the bot




def setup(bot):
    bot.add_cog(Traffichandle(bot))
