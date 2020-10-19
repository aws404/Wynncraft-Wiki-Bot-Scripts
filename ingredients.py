import wynn_api as api
import common
import sys
from river_mwclient.gamepedia_client import GamepediaClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

"""
Sprite overrides are first to be checked for the common.convert_sprite method.
If the name paramater matches a ket in this dict, it will be returned.
"""
# The api returns a player skull with a wither skeleton skin, providing that as an image would be redundant
sprite_overrides = {
    "Burnt Skull": "{{WynnIcon|wither skeleton skull}}",
    "Crumbling Skull": "{{WynnIcon|wither skeleton skull}}"
}

class IngredientInfoboxModifier(TemplateModifierBase):
    def update_template(self, template):
        if ":" in self.current_page.name:
            # Ignore if page is not in the default namespace
            return

        # The name to use for API-requests priorities: api-name (template param) > name (template param) > page name
        if template.has('api_name'):
            api_name = template.get('api_name').value.strip()
        elif template.has('name'):
            api_name = template.get('name').value.strip()
        else:
            api_name = self.current_page.name.strip()

        if api_name == "{{PAGENAME}}":
            api_name = self.current_page.name.strip()

        ingredient_data = api.get_ingredient(api_name)
        if ingredient_data is None:
            print(f"No API data was found for the ingredient with the API name '{api_name}' on the page '{self.current_page.name}'")
            return

        # Construction of new template data
        skills = ""
        for skill in ingredient_data['skills']:
            skills += str.lower(skill) + ","
            
        new_infobox_data = {'tier': ingredient_data['tier'],
                            'level': ingredient_data['level'],
                            'professions': skills,
                            }
        
        # Item name
        if 'displayName' in ingredient_data:
            new_infobox_data['name'] = ingredient_data['.displayName'].replace("֎", "")
        else:
            new_infobox_data['name'] = ingredient_data['name'].replace("֎", "")

        # Sprite data
        if api_name in sprite_overrides:
            # Use sprite from overrides dict
            new_infobox_data['image'] = sprite_overrides[api_name]
        elif template.has('image') and "." in template.get('image'):
            # Use pre-existing image
            new_infobox_data['image'] = template.get('image')
        else:
            # Get id:damage to namespaced_registry name
            new_infobox_data['image'] = common.convert_sprite(ingredient_data['sprite'].id, ingredient_data['sprite'].damage)

        # Apply new template data
        for data in new_infobox_data:
            template.add(data, new_infobox_data[data])


class IngredientCraftingModifier(TemplateModifierBase):
    def update_template(self, template):
        if ":" in self.current_page.name:
            # Ignore if page is not in the default namespace
            return

        # The name to use for API-requests priorities:
        # api-name (template param) > name (template param) > page name
        if template.has('api_name'):
            api_name = template.get('api_name').value.strip()
        elif template.has('name'):
            api_name = template.get('name').value.strip()
        else:
            api_name = self.current_page.name.strip()

        if api_name == "{{PAGENAME}}":
            api_name = self.current_page.name.strip()

        ingredient_data = api.get_ingredient(api_name)
        if ingredient_data is None:
            print(f"No API data was found for the ingredient with the API name '{api_name}' on the page '{self.current_page.name}'")
            return

        # Construction of new template data
        new_crafting_data = {**common.convert_range_identifications(ingredient_data['identifications']),
                             **common.convert_position_modifiers(ingredient_data['ingredientPositionModifiers'])
                            }
        if 'consumableOnlyIDs' in ingredient_data:
            new_crafting_data = new_crafting_data | common.convert_single_identifications(ingredient_data['consumableOnlyIDs'])

        if 'itemOnlyIDs' in ingredient_data:
            new_crafting_data = new_crafting_data | common.convert_single_identifications(ingredient_data['itemOnlyIDs'])

        # Item Name
        if 'displayName' in ingredient_data:
            new_crafting_data['name'] = ingredient_data['displayName'].replace("֎", "")
        else:
            new_crafting_data['name'] = ingredient_data['name'].replace("֎", "")

        # Sprite data
        if api_name in sprite_overrides:
            # Use sprite from overrides dict
            new_crafting_data['icon'] = sprite_overrides[api_name]
        elif template.has('icon') and "." in template.get('icon'):
            # Use pre-existing image
            new_crafting_data['icon'] = template.get('icon')
        else:
            # Convert id:damage to namespaced_registry name
            new_crafting_data['icon'] = common.convert_sprite(ingredient_data['sprite'].id, ingredient_data['sprite'].damage)

        # Apply new template data
        for data in new_crafting_data:
            template.add(data, new_crafting_data[data])


print("Connecting to Wynncraft Wiki...")
credentials = AuthCredentials(user_file="me")
wiki = GamepediaClient('wynncraft', credentials=credentials)
print("Connected!")

if len(sys.argv[1:]) > 0:
    IngredientInfoboxModifier(wiki, 'Infobox/Ingredient',
                              summary='Bot edit, update ingredient infobox template', title_list=sys.argv[1:]).run()
    IngredientCraftingModifier(wiki, 'Crafting',
                               summary='Bot edit, update ingredient crafting template', title_list=sys.argv[1:]).run()
else:
    IngredientInfoboxModifier(wiki, 'Infobox/Ingredient',
                              summary='Bot edit, update ingredient infobox template').run()
    IngredientCraftingModifier(wiki, 'Crafting',
                               summary='Bot edit, update ingredient crafting template').run()
