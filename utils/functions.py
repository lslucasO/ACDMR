import discord, requests, json
from bs4 import BeautifulSoup
from discord.ext import commands
from discord import app_commands


def createEmbed(embed_title, embed_field_name_list, embed_field_value_list, number_of_fields, embed_image_url=None):
    embed = discord.Embed(title=f"{embed_title}", color=discord.Color.blurple())
    embed.set_thumbnail(url=embed_image_url)
    
    for field in range(number_of_fields):   
        embed.add_field(name=f"{embed_field_name_list[field]}", value=f"{embed_field_value_list[field]}", inline=True)

    return embed  


def createProductEmbed(embed_title, embed_field_name_list, embed_field_value_list, number_of_value_fields, embed_image_url=None):
    embed = discord.Embed(title=f"{embed_title}", color=discord.Color.blurple())
    embed.set_thumbnail(url=embed_image_url)
    embed.add_field(name=f"{embed_field_name_list[0]}", value="",inline=False)
    
    for field in range(number_of_value_fields): 
        if int(embed_field_value_list[field]["stock"]) <= 50:   
            embed.add_field(name=f"{field+1}. **{embed_field_value_list[field]['product']}**", value=f"Estoque: **{embed_field_value_list[field]['stock']}** Unidades ⚠️\n Código: **{embed_field_value_list[field]['code']}**", inline=True)
        
    return embed


def getProduct(url):
    database = {}
    listData = []
    
    product_url = requests.get(url)
    doc = BeautifulSoup(product_url.text, "html.parser")
    
    product = doc.find("h1", class_="nome-produto titulo cor-secundaria").string
    price = doc.find("strong", class_="preco-promocional cor-principal titulo")
    stock = doc.find("b", class_="qtde_estoque").string
    image = doc.find("img", id="imagemProduto")
    code = doc.find("span", itemprop="sku").string
    
    product_information = [product, price["data-sell-price"], stock, image["src"], code]
    
    database["product"] = product
    database["code"] = code
    database["price"] = (price.string).strip()
    database["stock"] = stock.string
    database["image"] = image["src"]

    with open("database.json", "r") as f:
        data = json.load(f)  
        
        for produto in data:
            if database["product"] in produto["product"]:
                pass
            else:
         
                listData.append(produto)

        listData.append(database.copy())
              
    with open("database.json", "w") as f:
        json.dump(listData, f, indent=3)
        
    return product_information


#print(getProduct("https://www.gruposhopmix.com/moedor-de-carne-frango-profissional-eletrica-maquina-de-moer"))


def getStock():
    listProducts = []
    
    with open("database.json", "r") as f:
        data = json.load(f)  
        
        for produto in data:
            listProducts.append(produto)
            
    return listProducts
    

getStock()