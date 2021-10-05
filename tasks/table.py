import os
import json
import discord
import copy
from discord.ext import commands
from tabulate import tabulate


class Table(commands.Cog):
    """
    -->>> Works with Table <<<--
    """


    def __init__(self, bot):
        self.bot = bot
        self.update = True
        self.ch_msg = {}

        '''
        armor colors 0 = diff - | 1 = diff - | 2 = css [] | 3 = css [] | 4 = css [] | 5 = cs '' | 6 = diff +
        '''
        
    
    # Create titles to Populate text channels
    def create_msg(self, ch_name_only, data):
        
        try:# Creating Lines and Tabulate with Title
            title = ['Name', 'Dmg', 'Pen', 'ArmDmg%', 'Accu%', 'Rcoil', 'Frag.Chc']
            caliber = dmg = pen_power = arm_dmg = accrcy = recoil = frag_chce = []
            msg = {}
            try:# Comparing New vs Old JSON
                path_new_parsed = "./parsed/parsed_ammunition.json"# Saving New Parsed JSON
                path_old_parsed = "./parsed/old_parsed_ammunition.json"

                with open(path_new_parsed, "r") as new:# Opening New Parsed JSON
                    new_parsed = json.load(new)
                    
                with open(path_old_parsed, 'r') as old:# Opening Old Parsed JSON
                    old_parsed = json.load(old)

                
            except Exception as error:
                print(f"--> Error: Tables - Create Ammo - Comparing New vs Old JSON files. <--")
                print(error)

            # Enum data by ammo category
            for i, cat in enumerate(data):
                caliber.append(data[cat]['name'])
                text = []

                # Enum ammos in one category. j: name, dmg ...
                for j, name in enumerate(caliber[i]):
                    # Old Parsed
                    old_dmg = old_parsed[cat]['damage'][j]
                    old_pen_power = old_parsed[cat]['penetrationPower'][j]
                    old_arm_dmg = old_parsed[cat]['armorDamage'][j]
                    old_accrcy = old_parsed[cat]['accuracy'][j]# Green if positive, add +, else Red
                    old_recoil = old_parsed[cat]['recoil'][j]# Red if positive, add +, else Green
                    old_frag_chce = old_parsed[cat]['fragmentationChance'][j]# Show in %

                    old_parsed_elements = [old_dmg, old_pen_power, old_arm_dmg, old_accrcy, old_recoil, old_frag_chce]

                    # New Parsed
                    dmg = data[cat]['damage'][j]
                    pen_power = data[cat]['penetrationPower'][j]
                    arm_dmg = data[cat]['armorDamage'][j]
                    accrcy = data[cat]['accuracy'][j]# Green if positive, add +, else Red
                    recoil = data[cat]['recoil'][j]# Red if positive, add +, else Green
                    frag_chce = data[cat]['fragmentationChance'][j]# Show in %

                    new_parsed_elements = [dmg, pen_power, arm_dmg, accrcy, recoil, frag_chce]

                    
                    try:# Inserting signs, color and flags 🢁 🢃 🡅 🡇

                        if dmg == old_dmg:# Damage
                            ...
                        elif dmg > old_dmg:
                            dmg = f"{dmg}🡅"
                        else:
                            dmg = f"{dmg}🡇"
                        # End of Damage
                        
                        if pen_power == old_pen_power:# Penetration Power
                            ...
                        elif pen_power > old_pen_power:
                            pen_power = f"{pen_power}🡅"
                        else:
                            pen_power = f"{pen_power}🡇"
                        # End of Penetration Power
                        
                        if arm_dmg == old_arm_dmg:#Armor Damage
                            ...
                        elif arm_dmg > old_arm_dmg:
                            arm_dmg = f"{arm_dmg}🡅"
                        else:
                            arm_dmg = f"{arm_dmg}🡇"
                        #End of Armor Damage
                        
                        accrcy_str = accrcy# Accuracy
                        if accrcy > 0:
                            accrcy_str = f"+{accrcy}"
                        if accrcy == old_accrcy:
                            accrcy = accrcy_str
                        elif accrcy > old_accrcy:
                            accrcy = f"{accrcy_str}🡅"
                        else:
                            accrcy = f"{accrcy_str}🡇"
                        #End of Accuracy

                        recoil_str = recoil# Recoil
                        if recoil > 0:
                            recoil_str = f"+{recoil}"
                        if recoil == old_recoil:#recoil
                            recoil = recoil_str
                        elif recoil > old_recoil:
                            recoil = f"{recoil_str}🡅"
                        else:
                            recoil = f"{recoil_str}🡇"
                        # End of Recoil

                        frag_chce_str = f"{int(frag_chce * 100)}%"# Frag Chance
                        if frag_chce == old_frag_chce:
                            frag_chce = frag_chce_str
                        elif frag_chce > old_frag_chce:
                            frag_chce = f"{frag_chce_str}🡅"
                        else:
                            frag_chce = f"{frag_chce_str}🡇"
                        # End of Frag Chance


                    except Exception as error:
                        print("--> Error: Tables - Create Ammo - Creating Lines and Tabulate with Title - Inserting signs, color and flags. <--")
                        print(error)

                    # Creating list - Original values ->
                    # line = [data[cat]['name'][j], data[cat]['damage'][j], data[cat]['penetrationPower'][j], data[cat]['armorDamage'][j], data[cat]['accuracy'][j], data[cat]['recoil'][j], data[cat]['fragmentationChance'][j]]
                    line = [data[cat]['name'][j], dmg, pen_power, arm_dmg, accrcy, recoil, frag_chce]
                    
                    text.append(line)# Append list of line -> Text = list of lines
                
                '''
                table_fmts = ["plain", "simple", "github", "grid", "fancy_grid", "pipe", "orgtbl", "jira",
                "presto", "pretty", "psql", "rst", "mediawiki", "moinmoin", "youtrack", "html",
                "unsafehtml", "latex", "latex_raw","latex_booktabs", "latex_longtable", "textile", "tsv"]
                '''

                # Populate msg dict with 'ch_name_only' as keys
                # msg.update({ ch_name_only[i] : (tabulate(text, headers=title, tablefmt="presto", colalign="left", numalign="left")) })
                msg.update({ ch_name_only[i] : (tabulate(text, headers=title, tablefmt="pretty", colalign="left")) })

            return msg


        except Exception as error:
            print("--> Error: Tables - Create Ammo - Creating Lines and Tabulate with Title. <--")
            print(error)



    # Create titles to Populate text channels
    def check_update(self):
        
        try:# Check update
            diffkeys = []
            path_new_parsed = "./parsed/parsed_ammunition.json"# Saving New Parsed JSON
            path_old_parsed = "./parsed/old_parsed_ammunition.json"

            with open(path_new_parsed, "r") as new:# Opening New Parsed JSON
                new_parsed = json.load(new)
                
            with open(path_old_parsed, 'r') as old:# Opening Old Parsed JSON
                old_parsed = json.load(old)

            if new_parsed == old_parsed:# Comparing New vs Old JSON
                print("-> NO UPDATES <-")
            else:
                print("-> UPDATE! Old JSON file Updated!")
                diffkeys = [k for k in new_parsed if new_parsed[k] != old_parsed[k]]
            
            return diffkeys

        except Exception as error:
            print(f"--> Error: Tables - Check update. <--")
            print(error)



    # Create Ammo Tables
    async def create_ammo_table(self, ctx, ammo_cat, ch_name_only, calibers_name):
        
        try:
            p_file = "./parsed/parsed_ammunition.json"
            with open(p_file, 'r') as p:# Read the file
                data = json.load(p)

                # Whole discord text to send filtered by 'ch_name_only'
                msg = Table.create_msg(self, ch_name_only, data)

                # Create Ammo Table
                for cal in ch_name_only:
                    # Get Category
                    ammo_table = discord.utils.get(ctx.guild.channels, name=cal)

                    # Create new table ammo
                    if ammo_table == None:# Category is case sensitivity
                        ammo_table = await ctx.guild.create_text_channel(
                            cal,
                            category = ammo_cat,
                            sync_permissions=True
                        )

                        await ammo_table.send(f"`{msg[cal]}`")# Send as Code to ds
                    else:
                        await ammo_table.purge()# Clear chat
                        await ammo_table.send(f"`{msg[cal]}`")# Send as Code to ds


                print(f"Message sent to '{ch_name_only}' channels.")

            # Ammo Tables created: 12x70mm | 20x70mm | ... | 12.7x108mm.
            await ctx.send(f"Ammo Table created: `{' | '.join(str(c) for c in calibers_name)}`.")


        except Exception as error:
            await ctx.send("Oops... Not possible to create Ammo table.")
            print("--> Error: Tables - Create Ammo. <--")
            print(error)



    # Delete Ammo Tables
    async def delete_ammo_table(self, ctx, ammo_cat, ch_name_only):
        try:
            await ctx.send(f"Deleting Ammo Tables...")

            for cal in ch_name_only:
                ammo_table = discord.utils.get(ctx.guild.channels, name=cal)

                if ammo_table != None:# Category is case sensitivity
                    await ammo_table.delete()
                else:
                    print(f"Ammo Table: {ammo_table} not found.")

        except Exception as error:
            await ctx.send("Oops... Not possible to delete Ammo table.")
            print("--> Error: Tables - Not possible to delete Ammo table. <--")
            print(error)

    
    # Get Update Ammo Tables
    async def update_ammo_table(self, ctx, ammo_cat, ch_name_only, calibers_name):
        
        try:
            p_file = "./parsed/parsed_ammunition.json"
            with open(p_file, 'r') as p:# Read the file
                data = json.load(p)
            
            # New Recent Ammo updated
            diffkeys = Table.check_update(self)
            
            msg = Table.create_msg(self, ch_name_only, data)

            if len(diffkeys) > 0:# There is an update
                await ctx.send(f"Ammo Table updated: `{' | '.join(str(d) for d in diffkeys)}`.")

                # Filter different keys in calibers_name and get the correspondent in ch_name_only
                for d in diffkeys:
                    for i, c in enumerate(calibers_name):
                        if d == c:
                            upd_cal = ch_name_only[i]
                        
                            # Get Category
                            ammo_table = discord.utils.get(ctx.guild.channels, name=upd_cal)
                            # Create new updated ammo table
                            if ammo_table == None:# Category is case sensitivity
                                ammo_table = await ctx.guild.create_text_channel(
                                    upd_cal,
                                    category = ammo_cat,
                                    sync_permissions=True
                                )
                                await ammo_table.send(f"`{msg[upd_cal]}`")# Send as Code to ds as new ch
                            else:
                                await ammo_table.purge()# Clear chat
                                await ammo_table.send(f"`{msg[upd_cal]}`")# Send as Code to ds for existing ch

                # After updating Different Keys, save New as Old
                old_p_file = "./parsed/old_parsed_ammunition.json"
                with open(old_p_file, "w") as old:# Save New as Old.
                    json.dump(data, old)

            else:# Don't send msg
                await ctx.send(f"There is no Ammo Table update.")


        except Exception as error:
            await ctx.send("Oops... Not possible to update Ammo table.")
            print("--> Error: Tables - Update Ammo. <--")
            print(error)



    # Clear Update Ammo Table
    async def clear_update_ammo_table(self, ctx, ammo_cat, ch_name_only, calibers_name):
        
        try:
            path_new_parsed = "./parsed/parsed_ammunition.json"# Saving New Parsed JSON
            path_old_parsed = "./parsed/old_parsed_ammunition.json"

            with open(path_new_parsed, "r") as new:# Opening New Parsed JSON
                new_parsed = json.load(new)
                
            with open(path_old_parsed, 'r') as old:# Opening Old Parsed JSON
                old_parsed = json.load(old)

            with open(path_old_parsed, "w") as old:# Save New as Old.
                json.dump(new_parsed, old)
            
            await ctx.send(f"Update cleared.")

        except Exception as error:
            await ctx.send("Oops... Not possible to Clear Ammo Table Update.")
            print("--> Error: Tables - Clear Update Ammo Table. <--")
            print(error)


def setup(bot):
    bot.add_cog(Table(bot))
