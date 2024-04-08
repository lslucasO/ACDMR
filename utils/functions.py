import discord, requests, json
from bs4 import BeautifulSoup
from discord.ext import commands
from discord import app_commands


def createEmbed(embed_title, embed_field_name_list, embed_field_value_list, number_of_fields, embed_image_url=None):
    embed = discord.Embed(title=f"{embed_title}", color=discord.Color.blurple())
    embed.set_thumbnail(url=embed_image_url)
    
    for field in range(number_of_fields):   
        embed.add_field(name=f"{embed_field_name_list[field]}", value=f"{embed_field_value_list[field]}", inline=False)

    return embed  


def createProductEmbed(embed_title, embed_field_name_list, embed_field_value_list, number_of_value_fields, embed_image_url=None):
    embed = discord.Embed(title=f"{embed_title}", color=discord.Color.blurple())
    embed.set_thumbnail(url=embed_image_url)
    embed.add_field(name=f"{embed_field_name_list[0]}", value="",inline=False)
    
    for field in range(number_of_value_fields): 
        if int(embed_field_value_list[field]["stock"]) <= 50:   
            embed.add_field(name=f"{field+1}. **{embed_field_value_list[field]['product']}**", value=f"Estoque: **{embed_field_value_list[field]['stock']}** Unidades ⚠️\n Código: **{embed_field_value_list[field]['code']}**", inline=False)
        
    return embed


def saveProduct(product_information):
    
    database = {}
    listData = []

    database["product"] = product_information[0]
    database["code"] = product_information[4]
    database["price"] = product_information[1].strip()
    database["stock"] = product_information[2]
    database["image"] = product_information[3]
    database["url"] =product_information[5]
    
    with open("database/products.json", "r", encoding="utf-8") as f:
        data = json.load(f)  
        
        for produto in data:
            if database["product"] in produto["product"]:
                pass
            else:
                listData.append(produto)

        listData.append(database.copy())
     
    with open("database/products.json", "w", encoding="utf-8") as f:
        json.dump(listData, f, ensure_ascii=False, indent=3)


def getProduct(url):
    
    product_url = requests.get(url)
    doc = BeautifulSoup(product_url.text, "html.parser")
    
    product = doc.find("h1", class_="nome-produto titulo cor-secundaria").string
    price = doc.find("strong", class_="preco-promocional cor-principal titulo")
    stock = doc.find("b", class_="qtde_estoque").string
    image = doc.find("img", id="imagemProduto")
    code = doc.find("span", itemprop="sku").string
    product_information = [product, price["data-sell-price"], stock, image["src"], code, url]
        
    return product_information


def getStock():
    
    listProducts = []
    
    with open("database/products.json", "r", encoding="utf-8") as f:
        data = json.load(f)  
        
        for produto in data:
            listProducts.append(produto)
            
    return listProducts


def updateStock():

    listProducts = getStock()
    
    for product in listProducts:
        
        current_product = getProduct(product["url"])
        new_stock = int(current_product[2])
        old_stock = int(product["stock"])
        
        if new_stock < old_stock:
            # Tivemos uma venda
            sale = old_stock - new_stock
            # Estoque atual
            current_stock = old_stock - sale    
            # Atualizar o produto
            current_product[2] = current_stock
            saveProduct(current_product)
        else:
            pass
    
            
# produto = getProduct("https://www.gruposhopmix.com/tapete-antiderrapante-lava-pes-massageador-c-ventosas")
# saveProduct(produto)

