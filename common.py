import requests as r
import converter_maps as cm

print("Requesting legacy item id conversions...")
items_json = r.get("https://minecraft-ids.grahamedgecombe.com/items.json").json()
print("Complete! Items Loaded: " + str(len(items_json)))


def convert_sprite(numid: int, damage: int):
    """
    Convert the legacy numerical item ids to an sprite in the form of '{{ItemIcon|item name}}'
    :param name: Name of the item, used for sprite overrides
    :param previous: The previous value of the feild, if this is a [[File:file.png]] it will not be changed
    :param numid: The numerical id
    :param damage: The numerical damage value
    """
    for current in items_json:
        if numid == current['type'] and damage == current['meta']:
            name = current['name'].lower()
            return f'{{{{ItemIcon|{name}}}}}'

def format_number(num: int):
    if num > 0:
        num = '+' + str(num)
    else:
        num = str(num)
    
    return num

def convert_range_identifications(identifications: dict):
    """
    Convert any ranged value identifications to be in the form -min/+max
    :param identifications: The dict retrived from the v2 api
    """
    id_database = {}
    for id in identifications._data:
        wiki_name = cm.v2_to_wiki.get(id)

        min = format_number(identifications[id].minimum)
        max = format_number(identifications[id].maximum)

        id_database[wiki_name] = f"{min}/{max}"

    return id_database


def convert_single_identifications(identifications: dict):
    """
    Convert any singular value identifications to be in the correct template form
    :param identifications: The dict retrived from the v2 api
    """
    id_database = {}
    for id in identifications._data:
        value = identifications[id]
        if value == 0: continue

        wiki_name = cm.v2_to_wiki.get(id)
        id_database[wiki_name] = format_number(value)

    return id_database


def convert_position_modifiers(modifiers: dict):
    """
    Convert any position modifiers to be in the correct template form
    :param modifiers: The dict retrived from the v2 api
    """
    id_database = {}
    for mod in modifiers._data:
        value = modifiers[mod]
        if value == 0:
            continue

        value = format_number(value)

        if mod == "notTouching":
            mod = "not_touching"

        id_database["effectiveness_" + mod] = value

    return id_database
