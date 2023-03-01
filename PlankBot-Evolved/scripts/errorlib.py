import discord
from discord.ext import commands



class NotEnoughMoney(commands.CommandError):
    def __init__(self, amountShortness : int = 0) -> None:
        self.shortness = amountShortness


class NegativeParameter(commands.CommandError):
    def __init__(self) -> None:
        pass


class NoErrorsFound(commands.CommandError):
    def __init__(self) -> None:
        pass


class UnhandledException(commands.CommandError):
    def __init__(self, ctx : commands.Context, error, traceBack : str, message: str = None) -> None:
        super().__init__(message=message)
        self.ctx : commands.Context = ctx
        self.error = error
        self.traceback : str = traceBack


class BotUserMentioned(commands.CommandError):
    def __init__(self, mentionedBot : discord.Member, message: str = None) -> None:
        super().__init__(message=message)
        self.bot = mentionedBot


class UnknownBan(commands.CommandError):
    def __init__(self, user : discord.User, message: str = None) -> None:
        super().__init__(message=message)
        self.user: discord.User = user
        

class RolePositionTooSmall(commands.CommandError):
    def __init__(self, role : discord.Role, message: str = None) -> None:
        super().__init__(message=message)
        self.role: discord.Role = role

