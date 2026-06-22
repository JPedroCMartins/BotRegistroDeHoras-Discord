import discord
from discord import app_commands
from discord.ext import commands

from database.database import SessionLocal, Registro, agora, formatar_dt, formatar_duracao, formatar_segundos
from .config import Config
from . import comandos

class BotRegistroDeHoras(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)
        self.config = Config()

    async def on_ready(self):
        await self.tree.sync()
        print(f"✅ Bot do Discord online como {self.user}")

    async def setup_hook(self):
        comandos.Comandos(self.tree)

