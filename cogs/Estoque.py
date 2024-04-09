import discord, json
from time import sleep
from utils.functions import createEmbed, createProductEmbed, getProduct, getStock, saveDatabase, updateStock
from discord.ext import commands
from discord import app_commands

class Buttons(discord.ui.View):

    @discord.ui.button(label="Cadastrar",style=discord.ButtonStyle.green)
    async def cadastrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        self.message_product = await interaction.channel.send("Digite quantos produtos você deseja adicionar")
        self.quantity_product = await interaction.client.wait_for("message")
        self.msg_list = []
        self.url_list = []
        
        self.msg_list.append(self.message_product)
        self.msg_list.append(self.quantity_product)
        
        for self.index in range(int(self.quantity_product.content)):
            self.send_link = await interaction.followup.send(f"Manda o {self.index+1}* link")
            self.await_product = await interaction.client.wait_for("message")
            self.url = self.await_product.content
            self.msg_list.append(self.await_product)
            self.msg_list.append(self.send_link)
            
            # Peguei o produto
            self.product_information = getProduct(self.url)
            # Salvando na database
            saveDatabase(path="database/products.json", product=self.product_information)
            
            embed = createEmbed(embed_title=f"{self.product_information[0]}", embed_field_name_list=[f"Estoque:", f"Preço:"], embed_field_value_list=[f"{self.product_information[2]} Unidades", f"R${self.product_information[1]}"], number_of_fields=2, embed_image_url=f"{self.product_information[3]}")
            
            await interaction.followup.send(embed=embed)
        
        self.confirm_message = await interaction.followup.send("Produto **adicionado** com sucesso ")
        self.msg_list.append(self.confirm_message)
        
        
        embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"
        
        listProducts = getStock()

        embed = createProductEmbed(embed_title="Seu Estoque", embed_image_url=embed_image_url, embed_field_name_list=[f"Você tem **{len(listProducts)}** produtos cadastrados, mas apenas serão exibidos os que possuem pouco estoque."], embed_field_value_list=listProducts, number_of_value_fields=len(listProducts))
        self.view = Buttons(timeout=None)
        

        await interaction.followup.send(embed=embed, view=self.view)
        sleep(3)
        await interaction.delete_original_response()
        await interaction.channel.delete_messages(messages=self.msg_list)
    

    @discord.ui.button(label="Remover",style=discord.ButtonStyle.red)
    async def remover(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"
        self.i = 0
        self.msg_list = []
        self.listProducts = getStock()
        self.quantity_product = await interaction.channel.send("Digite o código do produto que deseja remover")
        self.remove_product = await interaction.client.wait_for("message")
        
        for self.product in self.listProducts:
            
            if self.product["code"] in str(self.remove_product.content):
                self.listProducts.pop(self.i)
                break
            else:
                self.i += 1
                    
        with open("database/products.json", "w", encoding="utf-8") as f:
            json.dump(self.listProducts, f, ensure_ascii=False, indent=3)
    
        self.confirm_message = await interaction.followup.send("Item removido com sucesso ✅")
        
        embed = createProductEmbed(embed_title="Seu Estoque", embed_image_url=embed_image_url, embed_field_name_list=[f"Você tem **{len(self.listProducts)}** produtos cadastrados, mas apenas serão exibidos os que possuem pouco estoque."], embed_field_value_list=self.listProducts, number_of_value_fields=len(self.listProducts))
        
        self.view = Buttons(timeout=None)
        
        self.msg_list.append(self.quantity_product)
        self.msg_list.append(self.remove_product)
        self.msg_list.append(self.confirm_message)
        
        
        await interaction.followup.send(embed=embed, view=self.view)
        sleep(3)
        await interaction.delete_original_response()
        await interaction.channel.delete_messages(messages=self.msg_list)
                    
                    
    @discord.ui.button(label="Estoque Total",style=discord.ButtonStyle.blurple)
    async def estoqueTotal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        self.msg_list = []
        with open('database/products.json', 'rb') as file:
            try:
                self.msg_file = await interaction.followup.send(file=discord.File(file))
            except FileNotFoundError:
                await interaction.followup.send("Arquivo não encontrado.")
        self.msg_list.append(self.msg_file)         
        sleep(30)
        await interaction.channel.delete_messages(messages=self.msg_list)
        
      
    @discord.ui.button(label="Atualizar Estoque",style=discord.ButtonStyle.secondary)
    async def atualizarEstoque(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        self.msg_list = []
        
        updateStock()
        self.confirm_message = await interaction.followup.send("Seu estoque foi atualizado com sucesso ✅")
        sleep(1)
        
        
        
        embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"
        listProducts = getStock()

        embed_relatorio = createEmbed(embed_title="Relatório de Vendas", embed_image_url=embed_image_url, embed_field_name_list=[f"{}"], embed_field_value_list=[f""], number_of_value_fields=len(listProducts))
        
        embed = createProductEmbed(embed_title="Seu Estoque", embed_image_url=embed_image_url, embed_field_name_list=[f"Você tem **{len(listProducts)}** produtos cadastrados, mas apenas serão exibidos os que possuem pouco estoque."], embed_field_value_list=listProducts, number_of_value_fields=len(listProducts))
        
        self.view = Buttons(timeout=None)
        
        self.msg_list.append(self.confirm_message)
        await interaction.followup.send(embed=embed, view=self.view)
        sleep(3)
        await interaction.delete_original_response()
        await interaction.channel.delete_messages(messages=self.msg_list)
        

class Estoque(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @app_commands.command(name="estoque", description="mostra seus produtos em estoque")
    async def estoque(self, interaction: discord.Interaction):
        
        await interaction.response.defer(ephemeral=False)
        embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"
        
        listProducts = getStock()
        
        embed = createProductEmbed(embed_title="Seu Estoque", embed_image_url=embed_image_url, embed_field_name_list=[f"Você tem {len(listProducts)} produtos cadastrados, mas apenas esses estão com pouco estoque."], embed_field_value_list=listProducts, number_of_value_fields=len(listProducts))
        
        self.view = Buttons(timeout=None)
        
        await interaction.followup.send(embed=embed, view=self.view)
           

async def setup(client):
    await client.add_cog(Estoque(client))