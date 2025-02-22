import csv, xml, json
import xml.etree.ElementTree as XET

# <card>
#     <name>001, Errant Spark-Engine</name>
#     <text>Menace, haste
# You may cast 001, Errant Spark-Engine from your graveyard by removing three loyalty counters from among permanents you control in addition to paying its other costs.</text>
#     <prop>
#         <side>front</side>
#         <manacost>2BG</manacost>
#         <cmc>4</cmc>
#         <colors>BG</colors>
#         <coloridentity>BG</coloridentity>
#         <layout>normal</layout>
#         <type>Legendary Artifact Creature — Construct</type>
#         <maintype>Creature</maintype>
#         <pt>4/4</pt>
#         <format-voyager>legal</format-voyager>
#     </prop>
#     <tablerow>2</tablerow>
#     <set num="81" rarity="rare">ITD</set>
# </card>


# {
#     ! "artist": "Jason Chan",
#     [cmc] "convertedManaCost": 3,
#     !/[cmc] "faceConvertedManaCost": 3,
#     [colors] "colors": [
#     "R"
#     ],
#     [coloridentity] "colorIdentity": [
#     "R"
#     ],
#     ! "designer": "Pipsqueak",
#     ! "flavor": "",
#     ! "frameType": "normal",
#     [NAME_SET]"id": "Academy Renegade_101",
#     [NAME.lower] "imageName": "academy renegade",
#     [layout] "layout": "normal",
#     [format-voyager] "legalities": [
#     {
#     "format": "MSEM2",
#     "legality": "Legal"
#     },
#     {
#     "format": "MSEDH",
#     "legality": "Legal"
#     }
#     ],
#     [manacost] "manaCost": "2R",
#     ! "multiverseid": 1,
#     [name] "name": "Academy Renegade",
#     [set (attr)] "number": "56",
#     [pt] "power": "2",
#     [set (attr)] "rarity": "rare",
#     ! "relatedCards": {
#     ! "spellbook": []
#     },
#     [type] "subtypes": [
#     "Human",
#     "Wizard"
#     ],
#     [text] "text": "When Academy Renegade enters, it deals damage to target creature you don't control equal to the number of Wizards you control.\nWhenever Academy Renegade attacks, it deals damage to defending player equal to the number of Wizards you control.",
#     [pt] "toughness": "2",
#     [type] "type": "Creature — Human Wizard",
#     [maintype] "types": [
#     "Creature"
#     ]
# }

def SlistFormat(string: str):
    out = ""
    for char in string:
        out += f'"{char}",'
    return out[:-1]

def LlistFormat(list_: list):
    out = ""
    for i in list_:
        out += f'"{i}",'
    return out[:-1]


SETS = {
    'VMN': ['Vinimroth Eternities', "2025-02-20"],
    'EXPT': ['Silver Core Set', "2025-02-20"],
    'PTN': ['Port Noon', "2025-02-20"],
    'ITD': ['Itera: Into the Dream', "2025-02-20"],
    'HTS': ['Hatsuniji', "2025-02-20"],
    'PVR': ['Primivir', "2025-02-20"],
    'AKT': ['Alkellan Transcendance' "2025-02-20"]
}

# Parse XML using ElementTree
tree = XET.parse("cardsources/cards.xml")
root = tree.getroot()
carddata = []

# Loop through XML and recatagorize the data into a python dictionary
for card in root[1]:
    #print(card.tag)
    carddict = {"related": []}
    for element in card: # Run through each element and assign the relevant carddict property
        #print(element)
        if element.tag == "name":
            carddict["name"] = element.text
        elif element.tag == "text":
            carddict["text"] = element.text
        elif element.tag == "set":
            carddict["set"] = element.text
            if "rarity" in element.attrib: carddict["rarity"] = element.attrib["rarity"]
            if "num" in element.attrib: carddict["num"] = element.attrib["num"]
        elif element.tag == "related":
            carddict["related"].append(element.text)
        elif element.tag == "prop": # Check for attributes in the <prop> element
            for property in element:
                if property.tag == "side":
                    carddict["face"] = property.text
                elif property.tag == "manacost":
                    carddict["cost"] = property.text
                elif property.tag == "cmc":
                    carddict["cmc"] = property.text
                elif property.tag == "colors":
                    carddict["colors"] = list(str(property.text))
                elif property.tag == "coloridentity":
                    carddict["colorident"] = list(str(property.text))
                elif property.tag == "layout":
                    carddict["layout"] = property.text
                elif property.tag == "type":
                    carddict["type"] = property.text
                elif property.tag == "maintype":
                    carddict["cardtype"] = property.text
                elif property.tag == "pt":
                    carddict["pt"] = property.text
    # print(carddict)
    carddata.append(carddict)
    
data = '{"meta":{},"data":{'
sortedCarddata = []

# Sort carddata by set
for set in SETS:
    cards = []
    for carddict in carddata:
        #print("looking", carddict)
        if carddict["set"] == set:
            cards.append(carddict)
    sortedCarddata.append({set: cards})

print(sortedCarddata)

setno = 0
# Convert newly sorted data into a string to write to JSON file
for set in sortedCarddata:
    data += f'"{set.keys()[0]}":{{"name":"{SETS[set.keys()[0]][0]}","code":"{set.keys()[0]}",releaseDate:"{SETS[set.keys()[0]][1]}","release_number":"{setno}","border":"black","type":"expert","booster":[],"mkm_name":"{SETS[set.keys()[0]][0]}","mkm_number":"{setno}","cards":['
    for card in set.values()[0]:
        data += f'"convertedManaCost":"{card["cmc"]}","colors":[{SlistFormat(card["colors"])}], "colorIdentity":[{SlistFormat(card["colorident"])}], "id":"{card["name"]}_{set.keys()[0].upper()}","imageName":"{card["name"]}","layout":"{card["layout"]}","legalities":[{{"format":"voyager","legality":"legal"}}],"manaCost":"{card["cost"]}",'
        if "pt" in card:
            data += f'"power":"{card["pt"].split("/")[0]}",'
        data += f'' # TODO, figure out related cards
        cardtypesplit = card["cardtype"].split(" ")
        cardtypesplit.remove("—")
        data += f'"subtypes":[{LlistFormat(card["type"].split("— ")[1].split(" "))}],"text":"{card["text"]}","toughness":"{card["pt"].split["/"][1]}","type":"{card["type"]}","types":[{LlistFormat(cardtypesplit)}]}},'
    data = data.rstrip(",")
    data += "}"

data += "}"
data += "}"

with open("AllCards.json", "w") as f:
    f.write(data)



#     [NAME_SET]"id": "Academy Renegade_101",
#     [NAME.lower] "imageName": "academy renegade",
#     [layout] "layout": "normal",
#     [manacost] "manaCost": "2R",
#     ! "multiverseid": 1,
#     [name] "name": "Academy Renegade",
#     [set (attr)] "number": "56",
#     [pt] "power": "2",
#     [set (attr)] "rarity": "rare",
#     ! "relatedCards": {
#     ! "spellbook": []
#     },
#     [type] "subtypes": [
#     "Human",
#     "Wizard"
#     ],
#     [text] "text": "When Academy Renegade enters, it deals damage to target creature you don't control equal to the number of Wizards you control.\nWhenever Academy Renegade attacks, it deals damage to defending player equal to the number of Wizards you control.",
#     [pt] "toughness": "2",
#     [type] "type": "Creature — Human Wizard",
#     [maintype] "types": [
#     "Creature"
#     ]
# }