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
            "quests":"https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/quests.json",
            #"traders":"https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/traders.json",
            #"hideout":"https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/hideout.json",
            "item_preset":"https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/item_presets.json",
            "items":"https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/items.en.json",
            "ammunition":"https://raw.githack.com/TarkovTracker/tarkovdata/master/ammunition.json"
        }
        # Quests
        self.quest_data = {}
        self.traders = {0:"Prapor", 1:"Therapist", 2:"Skier", 3:"Peacekeeper", 4:"Mechanic", 5:"Ragman", 6:"Jaeger", 7:"Fence"}
        self.locations = {
            "-2":"Any",
            "-1":"Any",
            "0":"Factory",
            "1":"Customs",
            "2":"Woods",
            "3":"Shoreline",
            "4":"Interchange",
            "5":"Labs",
            "6":"Reserve",
            "7":"Lighthouse"}
        # Ammunition
        self.ammunition_cal = {}
        self.ammunition_data = {
                    "kid":[],
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
                    # This is not working right now
                    # data = json.loads(data)
                    data = data.json()
                    name = "./json/" + k + ".json"

                    with open(name, 'w') as f:
                         json.dump(data, f, indent=2)

                    print(f"Data file created: {k}.json")

                try:# Removes the last JSON element of ammos - Wrong element -> '5485a8684bdc2da71d8b4567'
                    file = "./json/ammunition.json"
                    with open(file, 'r') as f:# Read the file
                        data = json.load(f)
                        del data['5485a8684bdc2da71d8b4567']

                    with open(name, 'w') as f:# Write the file back
                        json.dump(data, f, indent=2)

                    print(f"Data file edited: ammunition.json -> Removed last element: '5485a8684bdc2da71d8b4567'.")

                except Exception as error:
                    # await ctx.send("Ops... Deu algum erro!")
                    print("--> Error: Ammunition - Editing 'ammunition' json file. <--")
                    print(error)

        except Exception as error:
            # await ctx.send("Ops... Deu algum erro!")
            print("--> Error: Saving json file(s). <--")
            print(error)


        try:# Loading json files
            try:
                q = Query(self)# Get Query vars

            except Exception as error:
                print(f"--> Error: Getting Query. <--")
                print(error)
            

            for file in os.listdir("json"):
                if file.endswith(".json"):
                    print(f"'{file}' found.")
                    
                    if file == "ammunition.json":
                        try:
                            print(f"Parsing '{file}' file.")
                            await self.parse_ammo_json(file, q)# Parsing Ammunition JSON


                        except Exception as error:
                            print(f"--> Error: Parsing Ammunition json file: {file}. <--")
                            print(error)

                    elif file == "quests.json":
                        try:
                            print(f"Parsing '{file}' file.")
                            await self.parse_quests_json(file)# Parsing Quests JSON


                        except Exception as error:
                            print(f"--> Error: Parsing Quests json file: {file}. <--")
                            print(error)


        except Exception as error:
            # await ctx.send("Ops... Deu algum erro!")
            print("--> Error: No json file(s) found. <--")
            print(error)



    # Parsing Ammunition JSON file
    async def parse_ammo_json(self, file, q):
        try:
            calibers_raw = q.CALIBERS       # ["12/70", "20/70", ..., "12.7x108"]
            calibers_name = q.CALIBERS_NAME # ["12x70mm", "20x70mm", ..., "12.7x108mm"]

            for n in calibers_name:
                self.ammunition_cal.update({ n : copy.deepcopy(self.ammunition_data) })# Deep copy is required here, so the vals are not duplicated.
            #print(self.ammunition_cal)

            print(f"-> Calibers to parse: {calibers_raw}")


        except Exception as error:
            print(f"--> Error: Ammunition - Parsing JSON. <--")
            print(error)


        try:
            file = f"./json/{file}"
            with open(file, 'r') as f:# Open JSON as usual - Ammunition
                ammunition_data = json.load(f)
                
                for k_id in ammunition_data:# Pass through every element and store it.
                    kid                 = ammunition_data[k_id]['id']
                    name                = ammunition_data[k_id]['name']
                    shortName           = ammunition_data[k_id]['shortName']
                    weight              = ammunition_data[k_id]['weight']
                    caliber             = ammunition_data[k_id]['caliber']
                    stackMaxSize        = ammunition_data[k_id]['stackMaxSize']
                    tracer              = ammunition_data[k_id]['tracer']
                    tracerColor         = ammunition_data[k_id]['tracerColor']
                    ammoType            = ammunition_data[k_id]['ammoType']
                    projectileCount     = ammunition_data[k_id]['projectileCount']
                    damage              = ammunition_data[k_id]['ballistics']['damage']
                    armorDamage         = ammunition_data[k_id]['ballistics']['armorDamage']
                    fragmentationChance = ammunition_data[k_id]['ballistics']['fragmentationChance']
                    ricochetChance      = ammunition_data[k_id]['ballistics']['ricochetChance']
                    penetrationChance   = ammunition_data[k_id]['ballistics']['penetrationChance']
                    penetrationPower    = ammunition_data[k_id]['ballistics']['penetrationPower']
                    accuracy            = ammunition_data[k_id]['ballistics']['accuracy']
                    recoil              = ammunition_data[k_id]['ballistics']['recoil']
                    initialSpeed        = ammunition_data[k_id]['ballistics']['initialSpeed']

                    # Store all elements organized.
                    for ind, c_raw in enumerate(calibers_raw):# cal = calibers => calibers_name[i]
                        if c_raw in name:
                            self.ammunition_cal[calibers_name[ind]]['kid'].append(kid)
                            self.ammunition_cal[calibers_name[ind]]['name'].append(name)
                            self.ammunition_cal[calibers_name[ind]]['shortName'].append(shortName)
                            self.ammunition_cal[calibers_name[ind]]['weight'].append(weight)
                            self.ammunition_cal[calibers_name[ind]]['caliber'].append(caliber)
                            self.ammunition_cal[calibers_name[ind]]['stackMaxSize'].append(stackMaxSize)
                            self.ammunition_cal[calibers_name[ind]]['tracer'].append(tracer)
                            self.ammunition_cal[calibers_name[ind]]['tracerColor'].append(tracerColor)
                            self.ammunition_cal[calibers_name[ind]]['ammoType'].append(ammoType)
                            self.ammunition_cal[calibers_name[ind]]['projectileCount'].append(projectileCount)
                            self.ammunition_cal[calibers_name[ind]]['damage'].append(damage)
                            self.ammunition_cal[calibers_name[ind]]['armorDamage'].append(armorDamage)
                            self.ammunition_cal[calibers_name[ind]]['fragmentationChance'].append(fragmentationChance)
                            self.ammunition_cal[calibers_name[ind]]['ricochetChance'].append(ricochetChance)
                            self.ammunition_cal[calibers_name[ind]]['penetrationChance'].append(penetrationChance)
                            self.ammunition_cal[calibers_name[ind]]['penetrationPower'].append(penetrationPower)
                            self.ammunition_cal[calibers_name[ind]]['accuracy'].append(accuracy)
                            self.ammunition_cal[calibers_name[ind]]['recoil'].append(recoil)
                            self.ammunition_cal[calibers_name[ind]]['initialSpeed'].append(initialSpeed)
            '''
            # Debug
            for c in calibers_name:
                print(f"** {c} **")# calibers_name[0]
                print(f"{self.ammunition_cal[c]}")
            '''
            print(f"Parsed '{file}' file successfully.")


        except Exception as error:
            print(f"--> Error: Ammunition - Parsing JSON - Parsing JSON elements. <--")
            print(error)
                

        try:# Saving JSON.
            path_new_parsed = "./parsed/parsed_ammunition.json"# Saving New Parsed JSON
            with open(path_new_parsed, "w") as new:
                json.dump(self.ammunition_cal, new, indent=2)
                
            print(f"File '{path_new_parsed}' created.")
            
        except Exception as error:
            print(f"--> Error: Ammunition - Parsing JSON - Saving JSON. <--")
            print(error)



    # Parsing Quests JSON file
    async def parse_quests_json(self, file):
        try:
            # Load items into a JSON
            items_file = f"./json/items.json"
            with open(items_file, 'r') as item_f:# Open JSON as usual - Items
                item_data = json.load(item_f)

            items_preset_file = f"./json/item_preset.json"
            with open(items_preset_file, 'r') as item_p_f:# Open JSON as usual - Items Preset
                item_preset_data = json.load(item_p_f)

            # Load quests into a JSON
            file = f"./json/{file}"
            with open(file, 'r') as f:# Open JSON as usual - Quests
                quest_data = json.load(f)
                
                for quest in quest_data:# Pass through every element and store it.
                               
                    for key, value in quest.items():
                        if key == "giver":# Trader Name
                            quest[key] = self.traders[value]

                        elif key == "turnin":# Trader Name
                            quest[key] = self.traders[value]
                        
                        elif key == "require":# Quest Title, Trader Name
                            for req_key, req_value in quest['require'].items():
                                # Name of Quests instead of ID
                                if req_key == "quests" and len(quest['require']['quests']) > 0:# Replace Quest IDs for Titles
                                    for i, qid in enumerate(quest['require']['quests']):
                                        if type(qid) == list:# Checks if there is a list inside a list
                                            # print('its a list')
                                            for i, qid in enumerate(quest['require']['quests'][0]):# For inside that list
                                                for q in quest_data:
                                                    if qid == q['id']:
                                                        quest['require']['quests'][0][i] = q['title']
                                            quest['require']['quests'] = quest['require']['quests'][0] # Replace to 1 list only
                                        else:# If there is only 1 list
                                            for q in quest_data:
                                                if qid == q['id']:
                                                    quest['require']['quests'][i] = q['title']
                                    # print(f"Q[{quest['id']}]: {quest['require']['quests']}")

                                # Trader Name instead of ID
                                elif req_key == "loyalty":# Replace Loyalty trader number
                                    for i, loyals in enumerate(quest['require']['loyalty']):
                                        for k in loyals:
                                            if k == "trader":# Redundance in case it doesn't exist
                                                quest['require']['loyalty'][i][k] = self.traders[loyals[k]]
                                                # print(quest['require']['loyalty'][i])


                        elif key == "unlocks":# Items
                            if len(value) > 0:
                                for item in item_data:
                                    for i, unl in enumerate(quest['unlocks']):
                                        if unl == item:
                                            quest['unlocks'][i] = item_data[item]['name']
                                            # print(quest['unlocks'][i])
                                for item_p in item_preset_data:
                                    for j, unl2 in enumerate(quest['unlocks']):
                                        if unl2 == item_p:
                                            quest['unlocks'][j] = item_preset_data[item_p]['name']
                                            


                        elif key == "reputation":# trader
                            if len(value) > 0:
                                for i, rep in enumerate(quest['reputation']):
                                    for k in rep:
                                        if k == "trader":
                                            quest['reputation'][i][k] = self.traders[rep[k]]
                                            # print(quest['reputation'][i][k])


                        elif key == "reputationFailure":# trader
                            if len(value) > 0:
                                for i, rep in enumerate(quest['reputationFailure']):
                                    for k in rep:
                                        if k == "trader":
                                            quest['reputationFailure'][i][k] = self.traders[rep[k]]
                                            # print(quest['reputationFailure'][i][k])


                        elif key == "objectives":# location, tool, target
                            if len(value) > 0:
                                # Iterate in Objectives
                                for i, obj in enumerate(quest['objectives']):
                                    for k in obj:

                                        # Tool
                                        if k == 'tool':
                                            for item in item_data:# Pass through every element and store it.
                                                if obj[k] == item:# item = item_data[item]['id']
                                                    quest['objectives'][i][k] = item_data[item]['name']
                                                    # print(quest['objectives'][i]['tool'])
                                            # print(obj[k])

                                        # Location
                                        elif k == 'location':
                                            # print(self.locations[str(obj[k])])
                                            quest['objectives'][i][k] = self.locations[str(obj[k])]

                                        # Target
                                        if k == 'target':
                                            for item in item_data:# Pass through every element and store it.
                                                if type(obj[k]) == list:
                                                    #print(quest['objectives'][i])
                                                    for j, targ in enumerate(obj[k]):
                                                        if targ == item:
                                                            quest['objectives'][i][k][j] = item_data[item]['name']
                                                            # print(targ)
                                                            # print(quest['objectives'][i][k][j])
                                                else:
                                                    if obj[k] == item:# item = item_data[item]['id']
                                                        quest['objectives'][i][k] = item_data[item]['name']
                                                        # print(quest['objectives'][i]['tool'])
                                            # print(obj[k])


                        elif key == "alternatives":# By completing either xx or xx, you will fail and lose access to this quest.
                            if len(value) > 0:
                                for i, k in enumerate(quest['alternatives']):
                                    for q in quest_data:
                                        if k == q['id']:
                                            quest['alternatives'][i] = q['title']
                                            # print(f"{quest['alternatives'][i]}")


                self.quest_data = quest_data

        except Exception as error:
            print(f"--> Error: Quests - Parsing JSON. <--")
            print(error)


        try:# Saving Quests JSON.
            path_new_parsed = "./parsed/parsed_quests.json"# Saving New Parsed JSON
            with open(path_new_parsed, "w") as new:
                json.dump(self.quest_data, new, indent=2)
                
            print(f"File '{path_new_parsed}' created.")           

        except Exception as error:
            print(f"--> Error: Quests - Parsing JSON - Saving JSON. <--")
            print(error)


def setup(bot):
    bot.add_cog(Data(bot))
