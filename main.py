import os
import threading

from bot import BotRegistroDeHoras
from web import app
from dotenv import load_dotenv

load_dotenv()


def web():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT")), debug=os.getenv("DEBUG") == "True")

if __name__ == "__main__":

    web_server = threading.Thread(target=web, daemon=True)
    web_server.start()
    
    bot = BotRegistroDeHoras()
    bot.run(os.getenv("DISCORD_TOKEN"))