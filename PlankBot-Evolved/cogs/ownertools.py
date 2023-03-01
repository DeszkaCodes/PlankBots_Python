from datetime import datetime
import discord
from discord.ext import commands
from discord.ext.commands.core import guild_only
from data.database import db
from scripts.errorlib import NoErrorsFound
from scripts.helperlib import ErrorEmbed, PageOffset, ClosedEmbed, UnexpectedErrorEmbed
from scripts.settings import EmbedSettings
from scripts.helperlib import Clamp
from math import ceil
import traceback


class Ownertools(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        print("Owner Tools System Ready")


    #   Saved Errors Component

    class SaveErrorPageHandler(discord.ui.View):
        def __init__(self, maxPage : int, embed : discord.Embed, fieldEnder : str, entryPerPage : int, timeout: float = 180):
            super().__init__(timeout=timeout)
            self.page = 1
            self.maxPage = maxPage
            self.embed = embed
            self.entryPerPage = entryPerPage
            self.fieldEnder = fieldEnder

            if maxPage < 1:
                raise Exception("Maximum page must be more than 1.")

        @discord.ui.button(label="Előző oldal", style=discord.ButtonStyle.blurple)
        async def prevPage(self, button : discord.ui.Button, interaction : discord.Interaction):
            self.page = Clamp(self.page - 1, 1, self.maxPage)
            self.embed.set_footer(text=f"{self.page}/{self.maxPage}")

            await self.changePage()

            await interaction.response.edit_message(embed=self.embed)


        @discord.ui.button(label="Következő oldal", style=discord.ButtonStyle.blurple)
        async def nextPage(self, button : discord.ui.Button, interaction : discord.Interaction):
            self.page = Clamp(self.page + 1, 1, self.maxPage)
            self.embed.set_footer(text=f"{self.page}/{self.maxPage}")

            await self.changePage()

            await interaction.response.edit_message(embed=self.embed)

        @discord.ui.button(label="Kilépés", style=discord.ButtonStyle.red)
        async def exit(self, button : discord.ui.Button, interaction : discord.Interaction):

            await interaction.response.edit_message(embed=ClosedEmbed(), view=None)

            self.stop()

        async def changePage(self):
            self.embed.clear_fields()

            limitOffset = PageOffset(self.page, self.entryPerPage)
            errors = db.records("SELECT ID, MESSAGE, ERROR FROM UnhandledErrors LIMIT ? OFFSET ?", self.entryPerPage, limitOffset)

            for exception in errors:
                self.embed.add_field(
                        name=exception[1],
                        value=f"**Exception:** {exception[2]}\n**ID:** {exception[0]}{self.fieldEnder}",
                        inline=False
                    )

    class SaveErrorSpecific(discord.ui.View):
        def __init__(self, errorID : str, timeout: float = 180):
            super().__init__(timeout=timeout)
            self.id = errorID

        @discord.ui.button(label="Törlés", style=discord.ButtonStyle.red)
        async def delete(self, button : discord.ui.Button, interaction : discord.Interaction):
            db.execcommit("DELETE FROM UnhandledErrors WHERE ID = ?", self.id)

            embed=discord.Embed(title="Kezeletlen hiba törölve", description="Törölted a hibát az adatbázisból.", color=EmbedSettings.errorColor())
            embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
            embed.add_field(name="ID", value=self.id, inline=False)

            await interaction.response.edit_message(embed=embed, view=None)

            self.stop()

    @commands.group(invoke_without_command=True, aliases=["errors", "hibák", "hibak"])
    @commands.is_owner()
    @commands.guild_only()
    async def savedErrors(self, ctx : commands.Context):
        
        # Getting base page informations
        allEntries = db.field("SELECT COUNT(*) FROM UnhandledErrors")
        entriesPerPage = 5
        currentPage = 1
        limitOffset = PageOffset(currentPage, entriesPerPage)
        allPages = ceil(allEntries / entriesPerPage)


        # Setting up embed
        embed=discord.Embed(title="Kezeletlen hibák", description="A kezeletlen hibák listája", color=EmbedSettings.errorColor())
        embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
        embed.set_footer(text=f"{currentPage}/{allPages}")
        embedFieldEnder = "\n\n---------------------"

        errors = db.records("SELECT ID, MESSAGE, ERROR FROM UnhandledErrors LIMIT ? OFFSET ?", entriesPerPage, limitOffset)

        if not errors:
            raise NoErrorsFound()
        
        for exception in errors:
            embed.add_field(name=exception[1], value=f"**Exception:** {exception[2]}\n**ID:** {exception[0]}{embedFieldEnder}", inline=False)

        #Get view
        view = self.SaveErrorPageHandler(allPages, embed, embedFieldEnder, entriesPerPage)

        msg : discord.Message = await ctx.send(content=ctx.author.mention, embed=embed, view=view)

        await view.wait()

    @savedErrors.error
    async def savedErrors_error(self, ctx : commands.Context, error):
        if isinstance(error, NoErrorsFound):
            embed : discord.Embed= ErrorEmbed()
            embed.description = "Nincs kezeletlen hiba az adatbázisban."
            await ctx.send(content=ctx.author.mention, embed=embed)
        else:
            await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())


    @savedErrors.command(invoke_without_command=False)
    @commands.is_owner()
    async def specific(self, ctx : commands.Context, id : str):
        error = db.record("SELECT * FROM UnhandledErrors WHERE ID = ?", id)


        if not error:
            raise NoErrorsFound

        view = self.SaveErrorSpecific(errorID=error[0])

        embed=discord.Embed(title="Kezeletlen hiba", description="Megnyitottál egy kezeletlen hibát.", color=EmbedSettings.errorColor())
        embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())
        embed.add_field(name="ID", value=id, inline=False)
        embed.add_field(name="Parancs", value=error[1], inline=False)
        embed.add_field(name="Hiba", value=error[2], inline=False)
        if len(error[3]) >= 1024:
            allTracebacks : list[str] = error[3].split("The above exception was the direct cause of the following exception:")
            
            counter = 1
            for traceback in allTracebacks:
                embed.add_field(name=f"Traceback call part {counter}", value=traceback, inline=False)
                counter += 1
            
        else:
            embed.add_field(name="Traceback call", value=error[3], inline=False)

        await ctx.send(content=ctx.author.mention, embed=embed, view=view)

        await view.wait()

    @specific.error
    async def savedErrors_specific_error(self, ctx : commands.Context, error):
        if isinstance(error, NoErrorsFound):
            embed = ErrorEmbed("")
            embed.description="Nem találtunk hibát ezzel az azonosítóval."
            await ctx.send(content=ctx.author.mention, embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = ErrorEmbed("")
            embed.description=f"A(z) {error.param} paraméter nem lett megadva."
            await ctx.send(content=ctx.author.mention, embed=embed)
        else:
            await UnexpectedErrorEmbed(ctx, error, traceback.format_exc())

        await ctx.send(content=ctx.author.mention, embed=embed)
   
    # End of Saved Errors Component


def setup(bot):
    bot.add_cog(Ownertools(bot))
