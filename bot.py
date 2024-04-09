import discord, os, asyncio
import requests, json
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True 
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def on_message(message):
    if message.author.bot: 
        return

@client.event
async def on_ready():
    await client.tree.sync()    
    print(f"{client.user.name} is connected!")
    

async def load():   
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'{filename} is ready!')


async def main():
    async with client:
        await load()
        with open("./key.json", "r") as f:
            data = json.load(f)  
        await client.start(data["DISCORD_API_TOKEN"])


asyncio.run(main()) 