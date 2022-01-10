import os
import json
import discord
from discord.utils import get
from tabulate import tabulate
from discord.ext import commands
from reactionmenu import ReactionMenu, Button, ButtonType


class Quest(commands.Cog):
    """
    -->>> Works with Quest <<<--

    Fix "id": 9, mission Reputation with Traders/Numbers
    Add "hint": "Nighttime", to # Objectives
    Add "with": [],

    """

    def __init__(self, bot):
        self.bot = bot



    # Select all Quests
    async def all_quests(self, ctx):
        try:
            ...

        except Exception as error:
            print("--> Error: Quest - Not possible to Select All Quests. <--")
            print(error)


    
    # Create No Result Page
    async def create_no_result_page(self, ctx, option, count):
        try:
            embed_page = discord.Embed(
                description=f"{count} resultado(s)... 🚫",
                color=0x441CB9
            )
            embed_page.set_author(name=f"'{option}'", icon_url=self.bot.user.avatar_url)
            embed_page.set_footer(icon_url=self.bot.user.avatar_url)

            msg = await ctx.reply(embed=embed_page)
            await msg.add_reaction('👎')
        
        except Exception as error:
            print("--> Error: Quest - Not possible to Create Empty Embed Page. <--")
            print(error)
    


    # Create One Result Page
    async def create_one_result_page(self, ctx, option, count, q):
        try:
            # Only 1 Quest
            objectives = "-"
            if 'objectives' not in q or q['objectives'] == []:
                objectives = "?"
            else:
                objectives = q['objectives']

            # Check Trader Giver / Turnin
            g = q['giver']
            t = q['turnin']
            if g == t:
                gt = g
            else:
                gt = f"{g} / {t}"
            
            # Check Required Quests
            if len(q['require']['quests']) == 0:
                req_q = "No"
            else:
                req_q = ", ".join(str(rq) for rq in q['require']['quests'])
            
            # Check Level
            req_lvl = "No"
            if 'level' not in q['require'] or q['require']['level'] == '':
                req_lvl = "No"
            else:
                req_lvl = q['require']['level']

            # Creating Embed Page
            embed_page = discord.Embed(
                description=f"{count} resultado(s)...",
                color=0x441CB9
            )
            embed_page.set_author(name=f"'{option}'", icon_url=self.bot.user.avatar_url)
            embed_page.set_footer(icon_url=self.bot.user.avatar_url)

            # Title
            embed_page.add_field(name=f"{q['title']}", value=f"From/To: {gt} | Require: lvl {req_lvl} / Quest: {req_q}.", inline="False")

            # Objectives
            if objectives == '?':
                embed_page.add_field(name="Objectives", value=f" * {objectives}", inline="False")
            else:
                num = objectives[0]['number']
                if num != 1:
                    ...
                else:
                    num = ''
                typez = objectives[0]['type']
                if typez == 'key':
                    typez = 'Key needed: '
                
                loc = objectives[0]['location']
                if 'reputation' not in objectives[0] or loc == []:
                    loc = ''
            
                embed_page.add_field(name="Objectives", value=f" * {typez.capitalize()} {num} {objectives[0]['target']}. Map: {loc}", inline="False")
                if len(objectives) > 1:
                    for i, obj in enumerate(objectives):
                        if i == 0:
                            ...
                        else:
                            num = obj['number']
                            if num != 1:
                                ...
                            else:
                                num = ''

                            typez = obj['type']
                            if typez == 'key':
                                typez = 'Key needed: '

                            loc = obj['location']
                            if 'reputation' not in obj or loc == []:
                                loc = ''
                                
                            embed_page.add_field(name="\u200b", value=f" * {typez.capitalize()} {num} {obj['target']}. Map: {loc}", inline="False")

            # Rewards
            embed_page.add_field(name="Rewards", value=f" * {q['exp']} EXP.", inline="False")

            if 'reputation' not in q or q['reputation'] == []:
                ...
            else:
                for i, rep in enumerate(q['reputation']):
                    r = q['reputation'][i]['rep']
                    if r > 0:
                        r = f"+{q['reputation'][i]['rep']}"
                    embed_page.add_field(name="\u200b", value=f" * {q['reputation'][i]['trader']} Rep {r}.", inline="False")

            # Unlocks
            if q['unlocks'] == []:
                ...
            elif len(q['unlocks']) > 1:
                for i, unl in enumerate(q['unlocks']):
                    embed_page.add_field(name="\u200b", value=f" * {q['unlocks'][i]}.", inline="False")
            else:
                embed_page.add_field(name="Unlocks", value=f" * {q['unlocks'][0]}.", inline="False")

            # Link
            embed_page.add_field(name="Link", value=f"{q['wiki']}", inline="False")

            # await ctx.reply(embed=embed_page)
            return embed_page
        

        except Exception as error:
            print("--> Error: Quest - Not possible to Create One Result Page. <--")
            print(error)



    # Create Embed page for discord
    async def create_embed_page(self, ctx, option, quest):
        try:
                        

                ind = []
                count = 0

                # print(f"-> All Quests for '{option}'")
                # print(f"{len(ind)} Results")

                # for i, q in enumerate(quest):
                #     if option.lower() in q['title'].lower():
                #         ind.append(i)

                #         print(f"{i} - Q: {q['title']}")
                
                count = len(ind)
                if count > 0:
                    if count == 1:
                        try: # Results <= 1
                            print("Results == 1")
                            # Create One Page
                            q = quest[ind[0]]

                            embed_page = await Quest.create_one_result_page(self, ctx, option, count, q)

                            await ctx.reply(embed=embed_page)
                        
                        except Exception as error:
                            print(f"--> Error: Quest - Not possible to Create Embed Page - Results == 1. <--")
                            print(error)


                    else:# Pagination FIX
                        try: # Results > 1
                            print("Results > 1")

                            # Create all pages needed
                            tot_pages = count
                            pages = []

                            for page in range(0, tot_pages):
                                
                                q = quest[ind[page]]

                                embed_page = await Quest.create_one_result_page(self, ctx, option, count, q)

                                pages.append(embed_page)
                                

                            menu = ReactionMenu(ctx, back_button='◀️', next_button='▶️', config=ReactionMenu.STATIC)
                                
                            for embed_page in pages:
                                menu.add_page(embed_page)

                            # await ctx.send(embed=embed_page)
                            await menu.start()


                        except Exception as error:
                            print(f"--> Error: Quest - Not possible to Create Embed Page - Results > 1. <--")
                            print(error)


                else: # Results: 0
                    try:
                        await Quest.create_no_result_page(self, ctx, option, count)
                    
                    except Exception as error:
                            print(f"--> Error: Quest - Not possible to Create Embed Page - Results = 0. <--")
                            print(error)


        except Exception as error:
            print("--> Error: Quest - Not possible to Create Embed Page. <--")
            print(error)



    # Select all Quests for Option
    async def all_quests_option(self, ctx, option, quest):
        
        try:
            ...

        except Exception as error:
            print("--> Error: Not possible to Select All Quests for Option. <--")
            print(error)



    # Create Quest
    async def create_quest(self, ctx, option):
        
        try:# Create Quest
            # Load Quests
            quests = f"./parsed/parsed_quests.json"
            with open(quests, 'r') as f:# Open JSON as usual - Items
                quest = json.load(f)

                if option == 'all':
                    await ctx.reply(f"All Quests:")

                    await Quest.create_embed_page(self, ctx, quest)

                elif option == 'kappa':
                    await ctx.reply(f"All Quests for `'Kappa'`:")
                    await ctx.send(f"Kappa")
                else:
                    if len(option) < 3:# Check if input lenght is bigger than 3
                        await ctx.reply(f"Oops... Name: '{option}' deve conter pelo menos 3 letras.")
                    else:
                        try:
                            await ctx.reply(f"All Quests for `'{option}'`:")

                            await Quest.create_embed_page(self, ctx, option, quest)

                            # await menu.start()

                        except Exception as error:
                            print(f"--> Error: Quest - Not possible to find Quests. <--")
                            print(error)
                

        except Exception as error:
            await ctx.send("Oops... Not possible to create Quests.")
            print("--> Error: Quest - Not possible to create Quests. <--")
            print(error)


def setup(bot):
    bot.add_cog(Quest(bot))
