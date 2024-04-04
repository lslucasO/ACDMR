import discord
from utils.functions import createEmbed 
from discord.ext import commands
from discord import app_commands

class Buttons(discord.ui.View):

    @discord.ui.button(label="Cadastrar",style=discord.ButtonStyle.green)
    async def cadastrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("funciona")
                

       
        # self.view = Buttons(timeout=None)

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
        
        embed = createEmbed(embed_title="Seu Estoque", embed_image_url=embed_image_url, embed_field_name_list=["Produtos"], embed_field_value_list=["Teste"], number_of_fields=1)
        
        self.view = Buttons(timeout=None)
        
        await interaction.followup.send(embed=embed, view=self.view)
           

async def setup(client):
    await client.add_cog(Estoque(client))