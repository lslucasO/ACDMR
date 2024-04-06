import discord
from utils.functions import createEmbed, createProductEmbed, getProduct, getStock
from discord.ext import commands
from discord import app_commands

class Buttons(discord.ui.View):

    @discord.ui.button(label="Cadastrar",style=discord.ButtonStyle.green)
    async def cadastrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        self.message_product = await interaction.channel.send("Digite quantos produtos você deseja adicionar")
        self.quantity_product = await interaction.client.wait_for("message")
    
        self.url_list = []
        
        for self.index in range(int(self.quantity_product.content)):
            await interaction.followup.send(f"Manda o {self.index+1}* link")
            self.await_product = await interaction.client.wait_for("message")
            self.url = self.await_product.content
            
            self.product = getProduct(self.url)
            embed = createEmbed(embed_title=f"{self.product[0]}", embed_field_name_list=[f"Estoque:", f"Preço:"], embed_field_value_list=[f"{self.product[2]} Unidades", f"R${self.product[1]}"], number_of_fields=2, embed_image_url=f"{self.product[3]}")
            
            await interaction.followup.send(embed=embed)
        
        
        embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"
        
        listProducts = getStock()

        embed = createProductEmbed(embed_title="Seu Estoque", embed_image_url=embed_image_url, embed_field_name_list=[f"Você tem **{len(listProducts)}** produtos cadastrados"], embed_field_value_list=listProducts, number_of_value_fields=len(listProducts))
        self.view = Buttons(timeout=None)
        
        await interaction.followup.send(embed=embed, view=self.view)
                


    @discord.ui.button(label="Remover",style=discord.ButtonStyle.red)
    async def remover(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("funciona")
                    
            
        
        # self.view = Buttons(timeout=None)




class Estoque(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @app_commands.command(name="estoque", description="mostra seus produtos em estoque")
    async def estoque(self, interaction: discord.Interaction):
        
        await interaction.response.defer(ephemeral=False)
        embed_image_url = "https://cdn.discordapp.com/attachments/842737517228982272/1224822590061674546/20-01.png?ex=661ee3ed&is=660c6eed&hm=af4b36c7e87cac7b9f359fd8a65feaa8242f04f055ddeb30ad06261c49a3b178&"
        listProducts = getStock()
        
        
        
        embed = createProductEmbed(embed_title="Seu Estoque", embed_image_url=embed_image_url, embed_field_name_list=[f"Você tem **{len(listProducts)}** produtos cadastrados"], embed_field_value_list=listProducts, number_of_value_fields=len(listProducts))
        
        self.view = Buttons(timeout=None)
        
        await interaction.followup.send(embed=embed, view=self.view)
           

async def setup(client):
    await client.add_cog(Estoque(client))