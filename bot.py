import discord
from dotenv import load_dotenv
import os

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

token = os.getenv("DISCORD_BOT_TOKEN")
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


client.run(token)
