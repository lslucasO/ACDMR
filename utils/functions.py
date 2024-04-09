import discord, requests, json
from bs4 import BeautifulSoup
from discord.ext import commands
from discord import app_commands


def createEmbed(embed_title, embed_field_name_list, embed_field_value_list, number_of_fields, embed_image_url=None):
    embed = discord.Embed(title=f"{embed_title}", color=discord.Color.blurple())
    embed.set_thumbnail(url=embed_image_url)
    
    for field in range(number_of_fields):   
        print(field)
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


def saveDatabase(path, sales=None, product=None):
    
    database = {}
    listData = []
    
    if product:
        database["product"] = product[0]
        database["code"] = product[4]
        database["price"] = product[1].strip()
        database["stock"] = product[2]
        database["image"] = product[3]
        database["url"] =product[5]
    elif sales:
        for sale in sales:
            database["product"] = sale["product"]
            database["sale"] = sale["sales"]
        
    
    with open(f"{path}", "r", encoding="utf-8") as f:
        data = json.load(f)  
        
        for produto in data:
            if database["product"] in produto["product"]:
                pass
            else:
                listData.append(produto)

        listData.append(database.copy())
     
    with open(f"{path}", "w", encoding="utf-8") as f:
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
    sales = {}
    salesList = []
    
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
            
            sales["product"] = product["product"]
            sales["sales"] = sale
            
            saveDatabase(current_product)
        else:
            pass
    
    if len(salesList) == 0:
        pass
    else:
        salesList.append(sales.copy())
        saveDatabase(path="database/sales.json", sales=salesList)
    
    
    
 
    
def getSales():
    
    listSales = []
    
    with open("database/sales.json", "r", encoding="utf-8") as f:
        data = json.load(f)  
        
        for sale in data:
            listSales.append(sale)
            
    if len(listSales) == 0:
        listSales.append("Nenhum produto foi vendido hoje ;(")

    return listSales


         
# produto = getProduct("https://www.gruposhopmix.com/tapete-antiderrapante-lava-pes-massageador-c-ventosas")
# saveProduct(produto)

# print(len(getSales()))
# updateStock()
# print(getSales())

# listSales = getSales()

# embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"

# embed = createEmbed(embed_title="Relatório de Vendas", embed_image_url=embed_image_url, embed_field_name_list=[f"Você teve {len(listSales)} produtos vendidos"], embed_field_value_list=listSales, number_of_fields=len(listSales))
        