import discord, os, asyncio, random, datetime
import requests, bs4
from bs4 import BeautifulSoup
from time import sleep
from discord.ext import commands
from key import DISCORD_API_TOKEN

intents = discord.Intents.default()
intents.message_content = True 
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()    
    print(f"{client.user.name} is connected!")
    
    
@client.command()
async def produto(ctx, message):
    
    def getProduct(url):
        product_url = requests.get(url)
        doc = BeautifulSoup(product_url.text, "html.parser")
        
        product = doc.find("h1", class_="nome-produto titulo cor-secundaria").string
        price = doc.find("strong", class_="preco-promocional cor-principal titulo")
        stock = doc.find("b", class_="qtde_estoque").string
        
        message = f"""
        **Produto**: {product}
        **Preço**: R$ {price["data-sell-price"]}
        **Estoque**: {stock} 
        """
        
        return message


    
    await ctx.send(getProduct(f"{message}"))
    
    
async def load():   
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await client.load_extension(f'commands.{filename[:-3]}')
            print(f'{filename} is ready!')


async def main():
    async with client:
        await load()
        await client.start(DISCORD_API_TOKEN)


asyncio.run(main()) 