import discord, json
from time import sleep
from utils.functions import createEmbed, createProductEmbed, createSalesEmbed, getProduct, getSales, getStock, saveDatabase, updateStock
from discord.ext import commands
from discord import app_commands

class Cadastrar(discord.ui.View):

    @discord.ui.select(
        placeholder="Selecione quantos quer cadastrar...",
        options= [
            discord.SelectOption(label="1", value="1"),
            discord.SelectOption(label="5", value="5"),
            discord.SelectOption(label="10", value="10"),
            discord.SelectOption(label="50", value="50"),
            discord.SelectOption(label="100", value="100"),
        ]
    )
    
    async def cadastrar(self, interaction: discord.Interaction, select_item: discord.ui.Select):
        await interaction.response.defer()
        
        self.data = select_item.values
        self.msg_list = []
        self.url_list = []
        
        for self.index in range(int(self.data[0])):
            await interaction.followup.send(f"Manda o {self.index+1}* link", ephemeral=True)
            self.message = await interaction.client.wait_for("message", timeout=60.0)
            self.msg_list.append(self.message)
            
            self.message = self.message.content.split() 
            self.url = self.message[0]

            if len(self.message) == 4:
                self.color = self.message[1]
                self.size = self.message[2]
                self.stock = self.message[3]
                # Peguei o produto
                self.product_information = getProduct(url=self.url, color=self.color, size=self.size, stock=self.stock)
                # Salvando na database
                saveDatabase(path="database/products.json", product=self.product_information)
            elif len(self.message) == 3:
                self.color = self.message[1]
                self.size = self.message[2]
                self.product_information = getProduct(url=self.url, color=self.color, size=self.size)
                saveDatabase(path="database/products.json", product=self.product_information)
            elif len(self.message) == 2:
                self.color = self.message[1]
                self.product_information = getProduct(url=self.url, color=self.color)
                saveDatabase(path="database/products.json", product=self.product_information)
            else:
                self.product_information = getProduct(url=self.url)
                saveDatabase(path="database/products.json", product=self.product_information)
        
       
            
            embed = createEmbed(embed_title=f"{self.product_information[0]}", embed_field_name_list=[f"Estoque:", f"Preço:"], embed_field_value_list=[f"{self.product_information[2]} Unidades", f"R${self.product_information[1]}"], number_of_fields=2, embed_image_url=f"{self.product_information[3]}")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        
        await interaction.followup.send("Produto **adicionado** com sucesso", ephemeral=True)
        
        
        embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"
        
        listProducts = getStock()

        embed = createProductEmbed(embed_title="📦 Seu Estoque", embed_image_url=embed_image_url, embed_field_name_list=[f"Você tem {len(listProducts)} produtos cadastrados"], embed_field_value_list=listProducts, number_of_value_fields=len(listProducts))
        
        self.view = Buttons(timeout=None)
        

        await interaction.followup.send(embed=embed, view=self.view)
        await interaction.channel.delete_messages(messages=self.msg_list)
      
        
        

class Arquivo(discord.ui.View):

    @discord.ui.select(
        placeholder="Selecione qual arquivo quer consultar",
        options= [
            discord.SelectOption(label="📁 Produtos", value="1"),
            discord.SelectOption(label="💲 Vendas", value="2"),
        ]
    )
    
    async def arquivo(self, interaction: discord.Interaction, select_item: discord.ui.Select):
        await interaction.response.defer()
        
        self.data = select_item.values
        
        if int(self.data[0]) == 1:   
            self.path = "database/products.json"
        else:
            self.path = "database/sales.json"
        
        
        with open(f'{self.path}', 'rb') as file:
            try:
                self.msg_file = await interaction.followup.send(file=discord.File(file), ephemeral=True)
            except FileNotFoundError:
                await interaction.followup.send("Arquivo não encontrado.")


class Buttons(discord.ui.View):

    @discord.ui.button(label="🖥️ Cadastrar",style=discord.ButtonStyle.green)
    async def cadastrar(self, interaction: discord.Interaction, button: discord.ui.Button):                                                 
        await interaction.response.defer(ephemeral=True)
        
        self.view = Cadastrar()
        
        await interaction.followup.send(view=self.view)  
    
    

    @discord.ui.button(label="❌ Remover",style=discord.ButtonStyle.red)
    async def remover(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"
        i = 0
        self.msg_list = []
        self.listProducts = getStock()
        await interaction.followup.send("Digite o código do produto que deseja remover", ephemeral=True)
        self.remove_product = await interaction.client.wait_for("message", timeout=30)
        
        for self.product in self.listProducts:
            
            if self.product["code"] in str(self.remove_product.content):
                self.listProducts.pop(i)
                break
            else:
                i += 1
                    
        with open("database/products.json", "w", encoding="utf-8") as f:
            json.dump(self.listProducts, f, ensure_ascii=False, indent=3)
    
        await interaction.followup.send("Item removido com sucesso ✅", ephemeral=True)
        
        embed = createProductEmbed(embed_title="📦 Seu Estoque", embed_image_url=embed_image_url, embed_field_name_list=[f"Você tem {len(self.listProducts)} produtos cadastrados"], embed_field_value_list=self.listProducts, number_of_value_fields=len(self.listProducts))
        
        self.view = Buttons(timeout=None)
        
        self.msg_list.append(self.remove_product)
        
        await interaction.followup.send(embed=embed, view=self.view)
        sleep(3)
        await interaction.delete_original_response()
        await interaction.channel.delete_messages(messages=self.msg_list)
      
                    
    @discord.ui.button(label="🔃 Atualizar Estoque",style=discord.ButtonStyle.blurple)
    async def atualizarEstoque(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        
        updateStock()
        await interaction.followup.send("Seu estoque foi atualizado com sucesso ✅", ephemeral=True)
        
        listSales = getSales() 
        
        
        embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"

        
        embed = createSalesEmbed(embed_title="Relatório de Vendas", embed_image_url=embed_image_url, embed_field_name_list=[""], embed_field_value_list=listSales, number_of_fields=len(listSales))
        
        await interaction.followup.send(embed=embed, ephemeral=True)


    @discord.ui.button(label="💾 Arquivo",style=discord.ButtonStyle.gray)
    async def estoqueTotal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        self.view = Arquivo()
        
        self.msg_file = await interaction.followup.send(view=self.view, ephemeral=True)
       
       
class Estoque(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @app_commands.command(name="estoque", description="mostra seus produtos em estoque")
    async def estoque(self, interaction: discord.Interaction):
        
        await interaction.response.defer(ephemeral=False)
        embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"
        
        listProducts = getStock()
        
        embed = createProductEmbed(embed_title="📦 Seu Estoque", embed_image_url=embed_image_url, embed_field_name_list=[f"Você tem {len(listProducts)} produtos cadastrados"], embed_field_value_list=listProducts, number_of_value_fields=len(listProducts))
        
        self.view = Buttons(timeout=None)
        
        await interaction.followup.send(embed=embed, view=self.view)
           

async def setup(client):
    await client.add_cog(Estoque(client))