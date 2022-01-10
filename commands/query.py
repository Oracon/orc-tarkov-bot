import os
import discord
import json
from decouple import config
from discord.ext import commands
from tasks.table import Table
from tasks.category import Category
from tasks.quest import Quest
from tasks.tk import Tk


class Query(commands.Cog):
    """
    -->>> Works with Query <<<--

    !create ammo - Create category of tables all ammunition.
    """


    def __init__(self, bot):
        self.bot = bot

        self.AMMO_CAT_NAME = config("AMMO_CAT_NAME")# Discord Category name
        self.CALIBERS = config("CALIBERS")# Chosen based on JSON file 'name' to filter categories
        self.CALIBERS_NAME = config("CALIBERS_NAME")# table at https://escapefromtarkov.fandom.com/wiki/Ballistics
        self.CH_NAME_ONLY = config("CH_NAME_ONLY")# For creating and deleting ds channels only

        self.DS_USERS_TK = config("DS_USERS_TK")
        
        # str -> list
        self.CALIBERS = list(map(lambda x: x.split(',')[-1], json.loads(self.CALIBERS)))
        # self.CALIBERS = self.CALIBERS[5:7]# tests - ['12/70', '20/70']

        self.CALIBERS_NAME = list(map(lambda x: x.split(',')[-1], json.loads(self.CALIBERS_NAME)))
        # self.CALIBERS_NAME = self.CALIBERS_NAME[5:7] # test - ['12x70mm', '20x70mm']

        # DS text channel only
        self.CH_NAME_ONLY = list(map(lambda x: x.split(',')[-1], json.loads(self.CH_NAME_ONLY)))
        # self.CH_NAME_ONLY = self.CH_NAME_ONLY[5:7]
        

    # Create Ammo
    async def create_ammo(self, ctx):
        try:
            ammo_cat = await Category.create_ammo_category(self, ctx, self.AMMO_CAT_NAME)# Create Category
            await Table.create_ammo_table(self, ctx, ammo_cat, self.CH_NAME_ONLY, self.CALIBERS_NAME)# Create Ammo Table

        except Exception as error:
            await ctx.send("Oops... Not possible to create or find Category.")
            print("--> Error: Query - Not possible to create or find Category. <--")
            print(error)


    # Create TK
    # async def create_tk(self, ctx):
    #     try:
    #         ...
    #         await Tk.create_tk_table(self, ctx, self.DS_USERS_TK)

    #     except Exception as error:
    #         await ctx.send("Oops... Not possible to create or find Little TK table.")
    #         print("--> Error: Query - Not possible to create or find Little TK table. <--")
    #         print(error)
    


    # Delete Ammo
    async def delete_ammo(self, ctx):
        try:
            ammo_cat = discord.utils.get(ctx.guild.categories, name=self.AMMO_CAT_NAME)# Get Ammo Category
            await Table.delete_ammo_table(self, ctx, ammo_cat, self.CH_NAME_ONLY)# Delete Ammo Tables
            await Category.delete_ammo_category(self, ctx, ammo_cat, self.AMMO_CAT_NAME)# Delete Category
            
        except Exception as error:
            await ctx.send("Oops... Not possible to delete Ammo table.")
            print("--> Error: Query - Ammo table not deleted. <--")
            print(error)

    
    # Update Ammo
    async def update_ammo(self, ctx):
        try:
            ammo_cat = await Category.create_ammo_category(self, ctx, self.AMMO_CAT_NAME)# Create Category
            await Table.update_ammo_table(self, ctx, ammo_cat, self.CH_NAME_ONLY, self.CALIBERS_NAME)# Update Ammo Table

        except Exception as error:
            await ctx.send("Oops... Not possible to create or find Category.")
            print("--> Error: Query - Not possible to create or find Category. <--")
            print(error)

    
    # Clear Update Ammo
    async def clear_update_ammo(self, ctx):
        try:
            ammo_cat = await Category.create_ammo_category(self, ctx, self.AMMO_CAT_NAME)# Create Category
            await Table.clear_update_ammo_table(self, ctx, ammo_cat, self.CH_NAME_ONLY, self.CALIBERS_NAME)# Update Ammo Table

        except Exception as error:
            await ctx.send("Oops... Not possible to create or find Category.")
            print("--> Error: Query - Not possible to create or find Category. <--")
            print(error)


    # Quests
    async def show_quest(self, ctx, option):
        try:
            await Quest.create_quest(self, ctx, option)# Create Quest

        except Exception as error:
            await ctx.send("Oops... Not possible to show or find Quest.")
            print("--> Error: Query - Not possible to show or find Quest. <--")
            print(error)


    # Create Ammo Command
    @commands.command(aliases=['creates', 'c'], help="Creates table for the option selected. Arguments: 'ammo'.")
    async def create(self, ctx, option=''):
        try:
            if option == 'ammo':
                await self.create_ammo(ctx)
            else:#'ammo', 'maps', 'quests','traders', 'hideout', 'item_preset', 'items'
                await ctx.reply("No data selected. Please choose one option: `'ammo'`. and type `!create 'option'`.")
        
        except Exception as error:
            print("--> Error: Query - Command !create. <--")
            print(error)


    # Create TK Command - "async def create(self, ctx):" makes create ammo unusable
    # @commands.command(name="tk", help="Creates the Little TK table. No Arguments.")
    # async def create(self, ctx):
    #     try:
    #         await self.create_tk(ctx)
                    
    #     except Exception as error:
    #         print("--> Error: Query - Command !tk. <--")
    #         print(error)


    # Delete Ammo Command
    @commands.command(aliases=['deletes', 'del', 'd'], help="Deletes the whole Category for the option selected. Arguments: 'ammo'.")
    async def delete(self, ctx, option=''):
        try:
            if option == 'ammo':
                await self.delete_ammo(ctx)
            else:#'ammo', 'maps', 'quests','traders', 'hideout', 'item_preset', 'items'
                await ctx.reply("No data selected. Please choose one option: `'ammo'`. and type `!delete 'option'`.")
        
        except Exception as error:
            print("--> Error: Query - Command !delete. <--")
            print(error)


    # Update Ammo Command
    @commands.command(aliases=['updates', 'u'], help="Show or Clear Updates for option selected. Arguments: '', 'ammo', 'clear'.")
    async def update(self, ctx, option='ammo'):
        try:
            if option == 'ammo':# Update
                await self.update_ammo(ctx)
            elif option == 'clear':# Clear update
                await self.clear_update_ammo(ctx)
            else:#'ammo', 'maps', 'quests','traders', 'hideout', 'item_preset', 'items'
                await ctx.reply("No data selected. Please choose one option: `''`, `'ammo'` or `'clear'`. and type `!update 'option'`.")

        except Exception as error:
            print("--> Error: Query - Command !update. <--")
            print(error)
    

    # Quests Command
    @commands.command(aliases=['quests', 'q'], help="Show the Quests as commanded. Arguments: 'kappa'.")
    async def quest(self, ctx, option='', option2=''):
        try:
            if option != '':
                await self.show_quest(ctx, option)
            else:#'', 'all', 'kappa','lvl xx', 'item'
                await self.show_quest(ctx, option)
                # await ctx.reply("No data selected. Please choose one option: `'all'`, `'kappa'`, `'lvl'` or `'item'`. and type `!quest 'option'`.")
                await ctx.reply("No data selected. Please choose one option: `'all'`, `'kappa'` or `'text'`. and type `!quest 'option'`.")
        
        except Exception as error:
            print("--> Error: Query - Command !quest. <--")
            print(error)


def setup(bot):
    bot.add_cog(Query(bot))
