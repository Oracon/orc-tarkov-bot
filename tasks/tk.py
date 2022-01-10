import os
import json
import discord
import networkx as nx
import matplotlib.pyplot as plt
from discord.utils import get
from discord.ext import commands


class Tk(commands.Cog):
    """
    -->>> Works with Tk <<<--
    """

    def __init__(self, bot):
        self.bot = bot


    # Create Tk
    async def create_tk_table(self, ctx, ds_users_tk):
        
        try:
            await ctx.send(f"Tabilinha criada! User: {ds_users_tk}.")


            # Send @everyone, tk atualizado: @Orcon 🔪 -> @Oracon 💀

            

            G = nx.DiGraph()
            G.add_edges_from(
                [('A', 'B'), ('A', 'C'), ('D', 'B'), ('E', 'C'), ('E', 'F'),
                ('B', 'H'), ('B', 'G'), ('B', 'F'), ('C', 'G')])

            val_map = {'A': 1.0,
                    'D': 0.5714285714285714,
                    'H': 0.0}

            values = [val_map.get(node, 0.25) for node in G.nodes()]

            # Specify the edges you want here
            red_edges = [('A', 'C'), ('E', 'C')]
            edge_colours = ['black' if not edge in red_edges else 'red'
                            for edge in G.edges()]
            black_edges = [edge for edge in G.edges() if edge not in red_edges]

            # Need to create a layout when doing
            # separate calls to draw nodes and edges
            pos = nx.spring_layout(G)
            nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), 
                                node_color = values, node_size = 500)
            nx.draw_networkx_labels(G, pos)
            nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
            nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
            
            plt.show()
            
            '''
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
                await ctx.send(f"Tk table: `'{ammo_cat_name}'` created!")
            else:
                await ctx.reply(f"Tk: `'{ammo_cat_name}'`.")

            return ammo_cat# Returns Ammo Category to create tables
            '''
                    
        except Exception as error:
            await ctx.send("Oops... Not possible to create Little TK Table.")
            print("--> Error: TK not created. <--")
            print(error)


    # Delete Tk
    async def delete_tk(self, ctx):
        try:
            '''
            if ammo_cat == None:# Category is case sensitivity
                await ctx.reply(f"Category `'{ammo_cat_name}'` not found.")
            else:
                #ammo_cat = await ctx.guild.delete_category(ammo_cat_name)
                await ammo_cat.delete()
                await ctx.reply(f"Ammo Category: `'{ammo_cat}'` deleted!")
            '''

        except Exception as error:
            await ctx.send("Oops... Not possible to delete Little TK Table.")
            print("--> Error: TK not deleted. <--")
            print(error)


def setup(bot):
    bot.add_cog(Tk(bot))
