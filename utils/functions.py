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
    database["url"] = url
    
     
    with open("database.json", "r", encoding="utf-8") as f:
        data = json.load(f)  
        
        for produto in data:
            if database["product"] in produto["product"]:
                pass
            else:
                listData.append(produto)

        listData.append(database.copy())
              
    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(listData, f, ensure_ascii=False, indent=3)
        
    return product_information


# print(getProduct("https://www.gruposhopmix.com/cinta-calcinha-modeladora-aperta-barriga-alta-compressao-flores"))


def getStock():
    listProducts = []
    
    with open("database.json", "r", encoding="utf-8") as f:
        data = json.load(f)  
        
        for produto in data:
            listProducts.append(produto)
            
    return listProducts
    

# Função para corrigir a acentuação
def corrigir_acentuacao(texto):
    return texto.encode('latin1').decode('unicode_escape')

    # Carregar o arquivo JSON
    with open('dados.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    # Corrigir a acentuação
    for chave, valor in dados.items():
        dados[chave] = corrigir_acentuacao(valor)

    # Salvar de volta para o arquivo JSON
    with open('dados_corrigidos.json', 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)