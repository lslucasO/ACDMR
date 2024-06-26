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


def createSalesEmbed(embed_title, embed_field_name_list, embed_field_value_list, number_of_fields, embed_image_url=None):
    embed = discord.Embed(title=f"{embed_title}", color=discord.Color.blurple())
    
    embed.add_field(name=f"{embed_field_name_list[0]}", value="",inline=False)
    
    if embed_field_value_list[0] == "Nenhum produto foi vendido ;(":
        embed.add_field(name=f"", value=f"```{embed_field_value_list[0]}```",inline=False)
    else:
        for field in range(number_of_fields):
            embed.add_field(name=f"{field+1}", value=f"```📦 Produto: {embed_field_value_list[field]['product']}\n🏷️ Código: {embed_field_value_list[field]['code']}\n🟠 Cor: {embed_field_value_list[field]['color']}\n📏 Tamanho: {embed_field_value_list[field]['size']}\n💲 Vendas: {embed_field_value_list[field]['sales']} Unidades```", inline=False)
            

    return embed  


def createProductEmbed(embed_title, embed_field_name_list, embed_field_value_list, number_of_value_fields, embed_image_url=None):
    embed = discord.Embed(title=f"{embed_title}", color=discord.Color.blurple())
    embed.set_thumbnail(url=embed_image_url)
    embed.add_field(name=f"{embed_field_name_list[0]}", value="",inline=False)
    
    for field in range(number_of_value_fields): 
        if int(embed_field_value_list[field]["stock"]) <= 100:   
            embed.add_field(name=f"", value=f"```📦 Produto: {embed_field_value_list[field]['product']}\n🏷️ Código: {embed_field_value_list[field]['code']}\n🟢 Estoque: {embed_field_value_list[field]['stock']} Unidades ⚠️```", inline=False)
        
    return embed


def saveDatabase(path, method=None, sales=None, product=None):
    
    database = {}
    listData = []

    if product:
        database["product"] = product[0]
        database["code"] = product[4]
        database["price"] = float(product[1])
        database["stock"] = product[2]
        
        # color -> 6 len 7
        # size -> 7 len 8
        # pos -> 8 len 9
    
        if len(product) == 9:
            database["color"] = product[6].strip()
            database["size"] = product[7].strip()
            database["pos"] = product[8]
        elif len(product) == 8:
            if len(product[6]) <= 3:
                database["size"] = product[6].strip()
            else:
                database["color"] = product[6].strip()
            database["pos"] = product[7]

        else:
            database["color"] = ""
            database["size"] = ""
            database["pos"] = ""
            
        database["image"] = product[3]
        database["url"] =product[5]
        
        with open(f"{path}", "r", encoding="utf-8") as f:
            data = json.load(f)  
            
            for produto in data:
                if database["product"] in produto["product"] and database["color"] not in produto["color"]:
                    
                    # Mesmo produto, cor diferente
                    
                    listData.append(produto)
                elif database["product"] in produto["product"] and database["color"] in produto["color"] and database["size"] not in produto["size"]:
                    # Mesmo produto, cor igual, tamanho diferente
                    
                    listData.append(produto)
                elif database["product"] in produto["product"] and database["size"] in produto["size"] and database["color"] not in produto["color"]:
            
                    # Mesmo produto, tamanho igual, cor diferente
                    
                    listData.append(produto)
                elif database["product"] in produto["product"]:
                    pass
                else:
                    listData.append(produto)
            
            listData.append(database.copy())
        
    elif sales:
        listData = []
        listProducts = []
        found = False
        new = False
        i = 0
        duplicata = 0
        lenData = 0
            
        for sale in sales:
        
            database["product"] = sale["product"]
            database["code"] = sale["code"]
            database["color"] = sale["color"]
            database["size"] = sale["size"]
            database["sales"] = sale["sales"]  
            
            listData.append(database.copy()) 
            
            
    with open(f"{path}", "w", encoding="utf-8") as f:
        json.dump(listData, f, ensure_ascii=False, indent=3)


def getProduct(url, color=None, size=None, stock=None, pos=None):
    
    product_url = requests.get(url)
    doc = BeautifulSoup(product_url.text, "html.parser")
    
    product = doc.find("h1", class_="nome-produto titulo cor-secundaria").string
    price = doc.find("strong", class_="preco-promocional cor-principal titulo")
    found = False
    
    if stock:
        index = 1
        
        new_stock = doc.find_all("b", class_="qtde_estoque")
        
        for item in new_stock:
            #print(index)
            item = item.string
            # Achei o produto com o estoque especifico
            if pos != None:
                if index == pos:
                    #print(f"achei na {pos}* pos -> {item}")
                    found = True
                    stock = int(item)
                    break
            elif stock == int(item) and pos == None:
                found = True
                stock = int(item)
                break
            else:
                pass
            index += 1
        
    else:   
        stock = doc.find("b", class_="qtde_estoque")
        if stock == None:
            stock = 0
        else:
            stock = int(stock.string)
        
    image = doc.find("img", id="imagemProduto")
    code = doc.find("span", itemprop="sku").string 

    product_information = [product, price["data-sell-price"], stock, image["src"], code, url]

    if color and size:
        product_information.append(color.strip())
        product_information.append(size.strip())
        product_information.append(index)
    elif color:
        product_information.append(color)
        product_information.append(index)
    elif size:
        product_information.append(size)
        product_information.append(index)
    else:
        pass
    
    
    # print(product_information)
    
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
        # Requisitar novamente ao site
        if product["pos"] == "":
            current_product = getProduct(url=product["url"])
        else:
            current_product = getProduct(url=product["url"], stock=product["stock"], pos=product["pos"], color=product["color"], size=product["size"])
    
        # Estoque novo
        new_stock = int(current_product[2])
        # Antigo Estoque
        old_stock = int(product["stock"])
      
        if new_stock < old_stock:
            # Tivemos uma venda
            sale = old_stock - new_stock
            # Estoque atual
            current_stock = old_stock - sale    
            # Atualizar o produto
            current_product[2] = current_stock
            
            sales["product"] = product["product"]
            sales["code"] = product["code"]
            sales["color"] = product["color"]
            sales["size"] = product["size"]
            sales["sales"] = sale 
        
            salesList.append(sales.copy())
            
        saveDatabase(path="database/products.json", product=current_product)
        
    
    if len(salesList) == 0:
        print("Nenhum produto vendido !")
    else:
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



# print(getSales())
# updateStock()
# for c in range(3): 
#     pergunta = str(input("é comum? V/F: "))
    
#     if pergunta.upper() in "V":
#         product_url = str(input("url: "))
#         product_information = getProduct(url=product_url)
#     else:
#         product_url = str(input("url: "))
#         product_color = str(input("cor: "))
#         product_size = str(input("tamanho:"))
#         product_stock = int(input("estoque: "))
#         product_information = getProduct(url=product_url, color=product_color, size=product_size, stock=product_stock)
        
#     saveDatabase(path="database/products.json", product=product_information)
#     print("Produto cadastrado com sucesso")
    
    
# product_information = getProduct(url="https://www.gruposhopmix.com/produto/lanterna-led-de-cabeca-recarregavel-usb-resistente-agua.html")
# # # print(product_information)
# # product_information = getProduct(url="https://www.gruposhopmix.com/camisa-brasil-copa-do-mundo-torcedor-futebol", size="M", stock=6)
# # # # # product_information = getProduct(url="https://www.gruposhopmix.com/moedor-de-carne-frango-profissional-eletrica-maquina-de-moer")

# updateStock()
# saveProduct(produto)
# print(getSales())
# print(len(getSales()))
# updateStock()
# updateStock()
# print(getSales())

# listSales = getSales()
# # print(len(listSales))
# embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"
# print(len(listSales))
# embed = createSalesEmbed(embed_title="Relatório de Vendas", embed_image_url=embed_image_url, embed_field_name_list=[f""], embed_field_value_list=listSales, number_of_fields=len(listSales))
        