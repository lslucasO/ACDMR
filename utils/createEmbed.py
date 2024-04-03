import discord
from discord.ext import commands
from discord import app_commands


def createEmbed(embed_title, embed_field_name_list, embed_field_value_list, number_of_fields):
    embed = discord.Embed(title=f"{embed_title}", color=discord.Color.blurple())
    for field in range(number_of_fields):   
        embed.add_field(name=f"{embed_field_name_list[field]}", value=f"{embed_field_value_list[field]}", inline=False)
    
    return embed