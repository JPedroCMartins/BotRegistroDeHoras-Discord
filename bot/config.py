from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        self.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
        self.TIMEZONE = os.getenv("TIMEZONE")


