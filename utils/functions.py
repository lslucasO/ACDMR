import discord, requests
from bs4 import BeautifulSoup
from discord.ext import commands
from discord import app_commands


def createEmbed(embed_title, embed_image_url, embed_field_name_list, embed_field_value_list, number_of_fields):
    embed = discord.Embed(title=f"{embed_title}", color=discord.Color.blurple())
    embed.set_thumbnail(url=embed_image_url)
    
    for field in range(number_of_fields):   
        embed.add_field(name=f"{embed_field_name_list[field]}", value=f"{embed_field_value_list[field]}", inline=False)

    return embed


def getProduct(url):
    product_url = requests.get(url)
    doc = BeautifulSoup(product_url.text, "html.parser")
    
    product = doc.find("h1", class_="nome-produto titulo cor-secundaria").string
    price = doc.find("strong", class_="preco-promocional cor-principal titulo")
    stock = doc.find("b", class_="qtde_estoque").string
    
    message = f"""
    Produto: {product} \n
    Preço: R$ {price["data-sell-price"]} \n
    Estoque: {stock} 
    """
    
    return print(message)

