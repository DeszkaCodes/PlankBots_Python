#
#   This script file loads all the settings for the main file
#

import json
from dotenv import load_dotenv
import os


USE_STAGING_ENV : bool = True

path = f"data/environement/{'live' if not USE_STAGING_ENV else 'staging'}.env"
print(f"Env path: {path}")
load_dotenv(path)


# The class that will be sent to the other file
class Settings:
    @staticmethod
    def token() -> str:
        return os.getenv("BOT_TOKEN")


class EmbedSettings:
    @staticmethod
    def authorName() -> str:
        return os.getenv("EMBED_AUTHOR_NAME")

    @staticmethod
    def authorLink() -> str:
        return os.getenv("EMBED_AUTHOR_LINK")
    
    @staticmethod
    def authorIcon() -> str:
        return os.getenv("EMBED_AUTHOR_ICON")
        
    @staticmethod
    def defaultColor() -> int:
        return int(os.getenv("EMBED_DEFAULT_COLOR"), base=16)
        
    @staticmethod
    def moneyColor() -> int:
        return int(os.getenv("EMBED_MONEY_COLOR"), base=16)
        
    @staticmethod
    def errorColor() -> int:
        return int(os.getenv("EMBED_ERROR_COLOR"), base=16)
        
    @staticmethod
    def successColor() -> int:
        return int(os.getenv("EMBED_SUCCESS_COLOR"), base=16)

