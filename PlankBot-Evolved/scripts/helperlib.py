from random import random
from discord.ext import commands
from scripts.settings import EmbedSettings
from data.database import db
import discord, hashlib, time


# CLASSES

class TimeInSeconds:
    @staticmethod
    def Microsecond() -> float:
        return 0.000001
    
    @staticmethod
    def Millisecond() -> float:
        return 0.001
    
    @staticmethod
    def Second() -> int:
        return 1
    
    @staticmethod
    def Minute() -> int:
        return 60
    
    @staticmethod
    def Hour() -> int:
        return 3600
    
    @staticmethod
    def Day() -> int:
        return 86400
    
    @staticmethod
    def Week() -> int:
        return 604800
    
    @staticmethod
    def Year() -> int:
        return 31557600
        

# DEFINITIONS

def RandomInt(offSetInclusive : int, maxExclusive : int) -> int:
    return int(offSetInclusive + maxExclusive * random())


def ErrorEmbed(description : str = "") -> discord.Embed:
    embed=discord.Embed(title="Hibába ütköztünk", description=description, color=EmbedSettings.errorColor())
    embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())

    return embed


async def UnexpectedErrorEmbed(ctx : commands.Context, error, traceback : str) -> discord.Embed:
    embed = ErrorEmbed("Váratlan hiba")
    embed.add_field(name="Hiba kódja", value=error)
    embed.set_footer(text="A hibát lementettük az adatbázisunkba.")
    CommitError(ctx.message, error, traceback)

    await ctx.send(content=ctx.author.mention, embed=embed)


def CommitError(msg : discord.Message, error, traceback):

    message = msg.content

    unhashedID = message + str(int(time.time())) + str(error)

    id = hashlib.sha256(unhashedID.encode("utf-8")).hexdigest()

    db.execute(
            "INSERT OR IGNORE INTO UnhandledErrors (ID, MESSAGE, ERROR, TRACEBACK) VALUES (?, ?, ?, ?)",
            id,
            message,
            str(error),
            traceback
        )

    db.commit()


def PageOffset(currentPage : int, entryPerPage : int):
    return (currentPage - 1) * entryPerPage


def Clamp(number, minValue, maxValue):
   return max(min(number, maxValue), minValue)


def ClosedEmbed() -> discord.Embed:
    embed=discord.Embed(title="Ablak bezárva", description="Ez az ablak be lett zárva.", color=EmbedSettings.errorColor())
    embed.set_author(name=EmbedSettings.authorName(), url=EmbedSettings.authorLink(), icon_url=EmbedSettings.authorIcon())

    return embed


def MemberToEmbedAuthor(member : discord.Member) -> dict[str, str]:
    author : dict[str, str] = {"name": str(member),
                               "url": "https://discord.com/users/{member.id}",
                               "icon": str(member.avatar.url)}

    return author    



# END