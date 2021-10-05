import datetime
import requests
import os
import json
import copy
from decouple import config
import discord
from discord.ext import commands, tasks
from commands.query import Query
from tasks.table import Table



class Data(commands.Cog):
    """Work with data"""


    def __init__(self, bot):
        self.bot = bot
        self.d_links = {
            #"maps":"https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/maps.json",
            #"quests":"https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/quests.json",
            #"traders":"https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/traders.json",
            #"hideout":"https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/hideout.json",
            #"item_preset":"https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/item_presets.json",
            #"items":"https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/items.en.json",
            "ammunition":"https://raw.githack.com/TarkovTracker/tarkovdata/master/ammunition.json"
        }
        self.cal = {}
        self.data = {"kid":[],
                    "name":[],
                    "shortName":[],
                    "weight":[],
                    "caliber":[],
                    "stackMaxSize":[],
                    "tracer":[],
                    "tracerColor":[],
                    "ammoType":[],
                    "projectileCount":[],
                    "damage":[],
                    "armorDamage":[],
                    "fragmentationChance":[],
                    "ricochetChance":[],
                    "penetrationChance":[],
                    "penetrationPower":[],
                    "accuracy":[],
                    "recoil":[],
                    "initialSpeed":[]
                    }

        # ** -> 15 > projectileCount > 2
        # *** -> projectileCount >= 15
        # S -> subsonic: 33 - Except: 'grenade' and 'VOG-30' (41 total)
        # T -> Tracer - 16

    @commands.Cog.listener()
    async def on_ready(self):
        self.current_time.start()


    @tasks.loop(hours=24) # Save JSON files every 24h
    async def current_time(self):
        try:# Saving json files
            if len(self.d_links) == 0:
                print(f"-> NO DATA FILE CREATED! <-")
            else:
                for k in self.d_links:
                    url = self.d_links[f"{k}"]# Get url from dict
                    data = requests.get(url)
                    data = json.load(data)
                    name = "./json/" + k + ".json"

                    with open(name, 'w') as f:
                        json.dump(data, f)

                    print(f"Data file created: {k}.json")

                try:# Removes the last JSON element of ammos - Wrong element -> '5485a8684bdc2da71d8b4567'
                    file = "./json/ammunition.json"
                    with open(file, 'r') as f:# Read the file
                        data = json.load(f)
                        del data['5485a8684bdc2da71d8b4567']

                    with open(name, 'w') as f:# Write the file back
                        json.dump(data, f)

                    print(f"Data file edited: ammunition.json -> Removed last element: '5485a8684bdc2da71d8b4567'.")

                except Exception as error:
                    # await ctx.send("Ops... Deu algum erro!")
                    print("--> Error: Editing 'ammunition' json file. <--")
                    print(error)

        except Exception as error:
            # await ctx.send("Ops... Deu algum erro!")
            print("--> Error: Saving json file(s). <--")
            print(error)


        try:# Loading json files
            for file in os.listdir("json"):
                if file.endswith(".json"):
                    print(f"'{file}' found.")
                    
                    try:
                        print(f"Parsing '{file}' file.")
                        await self.parse_json(file)# Parsing JSON


                    except Exception as error:
                        print(f"--> Error: Parsing json file: {file}. <--")
                        print(error)


        except Exception as error:
            # await ctx.send("Ops... Deu algum erro!")
            print("--> Error: No json file(s) found. <--")
            print(error)



    # Parsing JSON file
    async def parse_json(self, file):
        try:
            q = Query(self)# Get Query vars
            calibers_raw = q.CALIBERS           # ["12/70", "20/70", ..., "12.7x108"]
            calibers_name = q.CALIBERS_NAME # ["12x70mm", "20x70mm", ..., "12.7x108mm"]

            for n in calibers_name:
                self.cal.update({ n : copy.deepcopy(self.data) })# Deep copy is required here, so the vals are not duplicated.
            #print(self.cal)
            file = f"./json/{file}"

            print(f"-> Calibers to parse: {calibers_raw}")


        except Exception as error:
            print(f"--> Error: Parsing JSON - Getting Query vars. <--")
            print(error)


        try:
            with open(file, 'r') as f:# Open JSON as usual
                data = json.load(f)
                
                for k_id in data:# Pass through every element and store it.
                    kid                 = data[k_id]['id']
                    name                = data[k_id]['name']
                    shortName           = data[k_id]['shortName']
                    weight              = data[k_id]['weight']
                    caliber             = data[k_id]['caliber']
                    stackMaxSize        = data[k_id]['stackMaxSize']
                    tracer              = data[k_id]['tracer']
                    tracerColor         = data[k_id]['tracerColor']
                    ammoType            = data[k_id]['ammoType']
                    projectileCount     = data[k_id]['projectileCount']
                    damage              = data[k_id]['ballistics']['damage']
                    armorDamage         = data[k_id]['ballistics']['armorDamage']
                    fragmentationChance = data[k_id]['ballistics']['fragmentationChance']
                    ricochetChance      = data[k_id]['ballistics']['ricochetChance']
                    penetrationChance   = data[k_id]['ballistics']['penetrationChance']
                    penetrationPower    = data[k_id]['ballistics']['penetrationPower']
                    accuracy            = data[k_id]['ballistics']['accuracy']
                    recoil              = data[k_id]['ballistics']['recoil']
                    initialSpeed        = data[k_id]['ballistics']['initialSpeed']

                    
                    # Store all elements organized.
                    for ind, c_raw in enumerate(calibers_raw):# cal = calibers => calibers_name[i]
                        if c_raw in name:
                            
                            self.cal[calibers_name[ind]]['kid'].append(kid)
                            self.cal[calibers_name[ind]]['name'].append(name)
                            self.cal[calibers_name[ind]]['shortName'].append(shortName)
                            self.cal[calibers_name[ind]]['weight'].append(weight)
                            self.cal[calibers_name[ind]]['caliber'].append(caliber)
                            self.cal[calibers_name[ind]]['stackMaxSize'].append(stackMaxSize)
                            self.cal[calibers_name[ind]]['tracer'].append(tracer)
                            self.cal[calibers_name[ind]]['tracerColor'].append(tracerColor)
                            self.cal[calibers_name[ind]]['ammoType'].append(ammoType)
                            self.cal[calibers_name[ind]]['projectileCount'].append(projectileCount)
                            self.cal[calibers_name[ind]]['damage'].append(damage)
                            self.cal[calibers_name[ind]]['armorDamage'].append(armorDamage)
                            self.cal[calibers_name[ind]]['fragmentationChance'].append(fragmentationChance)
                            self.cal[calibers_name[ind]]['ricochetChance'].append(ricochetChance)
                            self.cal[calibers_name[ind]]['penetrationChance'].append(penetrationChance)
                            self.cal[calibers_name[ind]]['penetrationPower'].append(penetrationPower)
                            self.cal[calibers_name[ind]]['accuracy'].append(accuracy)
                            self.cal[calibers_name[ind]]['recoil'].append(recoil)
                            self.cal[calibers_name[ind]]['initialSpeed'].append(initialSpeed)


            '''
            # Debug
            for c in calibers_name:
                print(f"** {c} **")# calibers_name[0]
                print(f"{self.cal[c]}")
            '''
            print(f"Parsed '{file}' file successfully.")


        except Exception as error:
            print(f"--> Error: Parsing JSON - Parsing JSON elements. <--")
            print(error)
                

        try:# Saving JSON.
            path_new_parsed = "./parsed/parsed_ammunition.json"# Saving New Parsed JSON
            with open(path_new_parsed, "w") as new:
                json.dump(self.cal, new)
                
            print(f"File '{path_new_parsed}' created.")
            
        except Exception as error:
            print(f"--> Error: Parsing JSON - Saving JSON. <--")
            print(error)


def setup(bot):
    bot.add_cog(Data(bot))
