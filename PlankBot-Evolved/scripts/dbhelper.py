import discord
from discord.ext import commands
from data.database import db

    
class LocalData:
    def __init__(self, user : discord.Member, balance : int, exp : int) -> None:
        self.serverID = user.guild.id
        self.userID = user.id
        self.balance = balance
        self.exp = exp

    @staticmethod
    async def DeleteUser(user : discord.Member):
        db.execcommit("DELETE FROM LocalData WHERE ServerID = ? AND ID = ?", user.guild.id, user.id)


    @classmethod
    async def GetData(cls, user : discord.Member):
        rawData = db.record("SELECT BALANCE,EXP FROM LocalData WHERE ServerID = ? AND ID = ?", user.guild.id, user.id)

        data : cls = None

        if not rawData:
            db.execcommit("INSERT OR IGNORE INTO LocalData (ServerID, ID, BALANCE, EXP) VALUES (?, ?, 0, 0)", user.guild.id, user.id)
            data = cls(user, 0, 0)

        else:
            data = cls(user, rawData[0], rawData[1])

        return data


class GlobalData:
    def __init__(self, user : discord.User, exp : int):
        self.userID = user.id
        self.exp = exp

    @classmethod
    async def GetData(cls, user : discord.User):
        rawData = db.record("SELECT EXP FROM GlobalData WHERE ID = ?", user.id)

        data : cls = None

        if not rawData:
            db.execcommit("INSERT OR IGNORE INTO GlobalData (ID, EXP) VALUES (?, ?)", user.id, 0)
            data = cls(user, 0, 0)

        else:
            data = cls(user, rawData[0])

        return data

    
class ServerData:
    def __init__(self, id : int, lvlChannel : int = None, trafficChannel : int = None) -> None:
        self.id : int = id
        self.lvlChannel : int = lvlChannel
        self.trafficChannel: int = trafficChannel
    
    @classmethod
    async def GetData(cls, guild : discord.Guild):
        rawData = db.record("SELECT * FROM ServerData WHERE ID = ?", guild.id)
        
        data : cls = None
        
        if not rawData:
            db.execcommit("INSERT OR IGNORE INTO ServerData (ID, LVLChannel, TrafficChannel) VALUES (?,?,?)", guild.id, None, None)
            
            data = cls(guild.id)
            
        else:
            data = cls(guild.id, rawData[1], rawData[2])
            
        return data
            
    