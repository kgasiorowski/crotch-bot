from bot.bot import bot
from config import secret

if __name__ == "__main__":
    bot.run(secret.AUTH_TOKEN)