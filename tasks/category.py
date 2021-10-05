import os
import json
import discord
from discord.utils import get
from discord.ext import commands


class Category(commands.Cog):
    """
    -->>> Works with Category <<<--
    """

    def __init__(self, bot):
        self.bot = bot


    # Create Category
    async def create_ammo_category(self, ctx, ammo_cat_name):
        
        try:# Create category
            ammo_cat = discord.utils.get(ctx.guild.categories, name=ammo_cat_name)
            
            if ammo_cat == None:# Category is case sensitivity
                ammo_cat = await ctx.guild.create_category(
                    ammo_cat_name,
                    overwrites={# Custom channel permissions.
                        ctx.guild.default_role: discord.PermissionOverwrite(
                            send_messages=False# By default, members can't send messages.
                        ),
                        ctx.guild.me: discord.PermissionOverwrite.from_pair(
                            discord.Permissions.all(),# But the bot has all permissions enabled...
                            discord.Permissions.none()# And none disabled!
                        )
                    },
                    reason='Only bot can send msg to this channel.'
                )
                await ctx.send(f"Ammo Category: `'{ammo_cat_name}'` created!")
            else:
                await ctx.reply(f"Category `'{ammo_cat_name}'`.")

            return ammo_cat# Returns Ammo Category to create tables
                    
        except Exception as error:
            await ctx.send("Oops... Not possible to create Ammo Category.")
            print("--> Error: Ammo Category not created. <--")
            print(error)


    # Delete Category
    async def delete_ammo_category(self, ctx, ammo_cat, ammo_cat_name):
        try:
            if ammo_cat == None:# Category is case sensitivity
                await ctx.reply(f"Category `'{ammo_cat_name}'` not found.")
            else:
                #ammo_cat = await ctx.guild.delete_category(ammo_cat_name)
                await ammo_cat.delete()
                await ctx.reply(f"Ammo Category: `'{ammo_cat}'` deleted!")

        except Exception as error:
            await ctx.send("Oops... Not possible to delete Ammo Category.")
            print("--> Error: Ammo Category not deleted. <--")
            print(error)


def setup(bot):
    bot.add_cog(Category(bot))
