import discord, os, asyncio
import requests, json
from discord.ext import commands
from utils.functions import createEmbed

intents = discord.Intents.default()
intents.message_content = True 
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())        

@client.event
async def on_ready():
    await client.tree.sync()    
    print(f"{client.user.name} is connected!")
    

@client.command()
async def regras(ctx):

    for guild in client.guilds:
        print(guild.name)
    channel = client.guilds[0].get_channel(1227712892095172769)
    print(channel)
    embed = createEmbed(embed_title=f"Formato", embed_field_name_list=[f"Como enviar a mensagem:", "Campos em Branco: "], embed_field_value_list=[f"```Envie a mensagem nesse formato:\nUrl Cor Tamanho Estoque```", "```Os campos que não existirem no produto preencha com -> ''. Só preencha o campo **Estoque** se o produto tiver algum desses atributos.```"], number_of_fields=2)
    
    await channel.send(embed=embed)


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