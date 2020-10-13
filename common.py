import requests
import converter_maps

print("Requesting legacy item id conversions...")
item_ids_data = requests.get("https://minecraft-ids.grahamedgecombe.com/items.json")
items_json = item_ids_data.json()
print("Complete! Items Loaded: " + str(len(items_json)))

sprite_overrides = {
    "Burnt Skull": "{{WynnIcon|wither skeleton skull}}",
    "Crumbling Skull": "{{WynnIcon|wither skeleton skull}}"
}

def convert_sprite( name, previous, numid, damage ):
    if name in sprite_overrides:
        return sprite_overrides[name]

    if "[[File:" in previous:
        return previous

    for current in items_json:
        if numid == current['type'] and damage == current['meta']:
            return '{{{{ItemIcon|{}}}}}'.format(current['name'].lower())

    return None

def convert_range_identifications( identifications ):
    ids = {}
    for id in identifications._data:
        wiki_name = converter_maps.id_map.get(id)
        max = identifications[id].maximum
        if max > 0:
            max = "+" + str(max)
        min = identifications[id].minimum
        if min > 0:
            min = "+" + str(min)
        ids[wiki_name] = "{}/{}".format(min, max)

    return ids

def convert_single_identifications( identifications ):
    ids = {}
    for id in identifications._data:
        value = identifications[id]
        if value == 0:
            continue

        if value > 0:
            value = "+" + str(value)

        wiki_name = converter_maps.id_map.get(id)
        ids[wiki_name] = value

    return ids

def convert_position_modifiers( modifiers ):
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
