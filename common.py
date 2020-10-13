import requests
import converter_maps

print("Requesting legacy item id conversions...")
item_ids_data = requests.get("https://minecraft-ids.grahamedgecombe.com/items.json")
items_json = item_ids_data.json()
print("Complete! Items Loaded: " + str(len(items_json)))

"""
Sprite overrides are first to be checked for the conver_sprite() method.
If the name paramater matches a ket in this dict, it will be returned.
"""
sprite_overrides = {
    "Burnt Skull": "{{WynnIcon|wither skeleton skull}}",
    "Crumbling Skull": "{{WynnIcon|wither skeleton skull}}"
}

def convert_sprite(name: str, previous: str, numid: int, damage: int):
    """
    Convert the legacy numerical item ids to an sprite in the form of '{{ItemIcon|item name}}'
    :param name: Name of the item, used for sprite overrides
    :param previous: The previous value of the feild, if this is a [[File:file.png]] it will not be changed
    :param numid: The numerical id
    :param damage: The numerical damage value
    """
    if name in sprite_overrides:
        return sprite_overrides[name]

    if "[[File:" in previous:
        return previous

    for current in items_json:
        if numid == current['type'] and damage == current['meta']:
            return '{{{{ItemIcon|{}}}}}'.format(current['name'].lower())

    return None

def convert_range_identifications(identifications: dict):
    """
    Convert any ranged value identifications to be in the form -min/+max
    :param identifications: The dict retrived from the v2 api
    """
    ids = {}
    for id in identifications._data:
        wiki_name = converter_maps.v2_to_wiki.get(id)
        max = identifications[id].maximum
        if max > 0:
            max = "+" + str(max)
        min = identifications[id].minimum
        if min > 0:
            min = "+" + str(min)
        ids[wiki_name] = "{}/{}".format(min, max)

    return ids

def convert_single_identifications(identifications: dict):
    """
    Convert any singular value identifications to be in the correct template form
    :param identifications: The dict retrived from the v2 api
    """
    ids = {}
    for id in identifications._data:
        value = identifications[id]
        if value == 0:
            continue

        if value > 0:
            value = "+" + str(value)

        wiki_name = converter_maps.v2_to_wiki.get(id)
        ids[wiki_name] = value

    return ids

def convert_position_modifiers(modifiers: dict):
    """
    Convert any position modifiers to be in the correct template form
    :param identifications: The dict retrived from the v2 api
    """
    ids = {}
    for mod in modifiers._data:
        value = modifiers[mod]
        if value == 0:
            continue

        if value > 0:
            value = "+" + str(value)

        if mod == "notTouching":
            mod = "not_touching"

        ids["effectiveness_" + mod] = value

    return ids
