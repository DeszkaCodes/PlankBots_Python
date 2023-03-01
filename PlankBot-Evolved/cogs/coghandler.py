import discord
from discord.ext import commands
from scripts.settings import EmbedSettings
from scripts.helperlib import UnexpectedErrorEmbed, Clamp, ClosedEmbed
import traceback


class Coghandler(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        self.cogs : dict = {}
        print("Cog Handler System Ready")
    
    @commands.Cog.listener()
    async def on_ready(self):
        for extension in self.bot.extensions.keys():
            self.cogs.setdefault(extension[5:], True)

        print("Cogs Saved")
        

    class CogsUI(discord.ui.View):
        def __init__(self, bot : commands.Bot, extensions : dict, timeout: float = 180):
            super().__init__(timeout=timeout)

            self.extensions : dict = extensions
            self.bot = bot
            self.selected : int = 0
            self.selector : str = " <-- KIJELÖLVE"

            self.embed = discord.Embed(title="Cog menü", description="Cog kezelőmenü.", color=EmbedSettings.defaultColor())
            self.embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())

            for extension in self.extensions:
                if extension == "coghandler":
                    continue

                self.embed.add_field(name=f"{extension.capitalize()}", value="Aktív" if extensions[extension] else "Inaktív", inline=False)

            self.embed.set_field_at(
                    0,
                    name=f"{self.embed.fields[0].name}{self.selector}",
                    value="Aktív" if extensions[extension] else "Inaktív",
                    inline=False
                )


        @discord.ui.button(label="Le", style=discord.ButtonStyle.blurple)
        async def down(self, button : discord.ui.Button, interaction : discord.Interaction):
            self.embed.set_field_at(
                    self.selected,
                    name=f"{self.embed.fields[self.selected].name[:-len(self.selector)]}",
                    value=self.embed.fields[self.selected].value,
                    inline=False
                )

            self.selected = Clamp(self.selected + 1, 0, len(self.embed.fields)-1)

            self.embed.set_field_at(
                    self.selected,
                    name=f"{self.embed.fields[self.selected].name}{self.selector}",
                    value=self.embed.fields[self.selected].value,
                    inline=False
                )

            await interaction.response.edit_message(embed=self.embed)


        @discord.ui.button(label="Fel", style=discord.ButtonStyle.blurple)
        async def up(self, button : discord.ui.Button, interaction: discord.Interaction):
            self.embed.set_field_at(
                    self.selected,
                    name=f"{self.embed.fields[self.selected].name[:-len(self.selector)]}",
                    value=self.embed.fields[self.selected].value,
                    inline=False
                )

            self.selected = Clamp(self.selected - 1, 0, len(self.embed.fields)-1)

            self.embed.set_field_at(
                    self.selected,
                    name=f"{self.embed.fields[self.selected].name}{self.selector}",
                    value=self.embed.fields[self.selected].value,
                    inline=False
                )

            await interaction.response.edit_message(embed=self.embed)


        @discord.ui.button(label="Betölt/Kikapcsol", style=discord.ButtonStyle.blurple)
        async def load(self, button : discord.ui.Button, interaction: discord.Interaction):

            # TO UNDERSTAND: we get the selected field with the self.selected
            # TO UNDERSTAND: then we cut off the selector by getting the legth of it
            # TO UNDERSTAND: and at last we lower it so it will be the correct key
            currentCog = self.embed.fields[self.selected].name[:-len(self.selector)].lower()
            isLoaded : bool = self.extensions[currentCog]

            if isLoaded:
                self.bot.unload_extension(f"cogs.{currentCog}")
            else:
                self.bot.load_extension(f"cogs.{currentCog}")

            self.extensions[currentCog] = not isLoaded

            self.embed.set_field_at(
                self.selected,
                name = self.embed.fields[self.selected].name,
                value = "Aktív" if not isLoaded else "Inaktív",
                inline=False
            )

            await interaction.response.edit_message(embed=self.embed)
            
        @discord.ui.button(label="Újraindít", style=discord.ButtonStyle.blurple)
        async def reload(self, button : discord.ui.Button, interaction: discord.Interaction):

            # TO UNDERSTAND: we get the selected field with the self.selected
            # TO UNDERSTAND: then we cut off the selector by getting the legth of it
            # TO UNDERSTAND: and at last we lower it so it will be the correct key
            currentCog = self.embed.fields[self.selected].name[:-len(self.selector)].lower()
            isLoaded : bool = self.extensions[currentCog]

            if isLoaded:
                self.bot.unload_extension(f"cogs.{currentCog}")
            
            self.bot.load_extension(f"cogs.{currentCog}")

            self.extensions[currentCog] = True

            self.embed.set_field_at(
                self.selected,
                name = self.embed.fields[self.selected].name,
                value = "Újra indítva",
                inline=False
            )

            await interaction.response.edit_message(embed=self.embed)

        @discord.ui.button(label="Kilépés", style=discord.ButtonStyle.red)
        async def exit(self, button : discord.ui.Button, interaction : discord.Interaction):

            await interaction.response.edit_message(embed=ClosedEmbed(), view=None)

            self.stop()


    @commands.command()
    @commands.is_owner()
    async def cogs(self, ctx : commands.Context):
        view = self.CogsUI(self.bot, self.cogs)

        await ctx.send(content=ctx.author.mention, embed=view.embed, view=view)

        await view.wait()


    

def setup(bot):
    bot.add_cog(Coghandler(bot))
