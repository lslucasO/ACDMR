import discord
from utils.createEmbed import createEmbed 
from discord.ext import commands
from discord import app_commands


class Estoque(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @app_commands.command(name="estoque", description="mostra seus produtos em estoque")
    async def estoque(self, interaction: discord.Interaction):
        
        await interaction.response.defer(ephemeral=False)
        
        embed_field_name_list = ["Produtos"]
        embed_field_value_list = ["Teste"]
        embed = createEmbed(embed_title="Estoque de Produtos", embed_field_name_list=embed_field_name_list, embed_field_value_list=embed_field_value_list, number_of_fields=1)
        
        # self.view = Buttons(timeout=None)
        
        await interaction.followup.send(embed=embed)
           

async def setup(client):
    await client.add_cog(Estoque(client))