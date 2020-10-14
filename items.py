import wynn
import common
import sys
import converter_maps
import math
from river_mwclient.gamepedia_client import GamepediaClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

class InfoboxModifier(TemplateModifierBase):
    def update_template(self, template):
        if ":" in self.current_page.name:
            # Ignore if page is not in the default namespace
            return

        # The name to use for API-requests priorities: api-name (template param) > name (template param) > page name
        api_name = template.get('api_name').value.strip() if template.has('api_name') else template.get('name').value.strip() if template.has('name') else self.current_page.name.strip()
        if api_name == "{{PAGENAME}}":
            api_name = self.current_page.name.strip()

        items_list = wynn.item.search_item(name=api_name)
        if items_list == None:
            print("No API data was found for the item with the API name '{}' on the page '{}' (Nothing on search)".format(api_name, self.current_page.name))
            return
        item_data = None
        for current_item in items_list:
            if current_item.name == api_name or ('displayName' in current_item and current_item.displayName == api_name):
                item_data = current_item
                break
        if item_data == None:
            print("No API data was found for the item with the API name '{}' on the page '{}' (Not found in search)".format(api_name, self.current_page.name))
            return

        # Construction of new template data
        for key in item_data._data:
            if item_data[key] and item_data[key] != None and item_data[key] != "0-0" and item_data[key] != 0:
                if key in converter_maps.item_info_box:
                    template_key = converter_maps.item_info_box[key]
                    template_value = item_data[key]
                    if isinstance(template_value, str):
                        template_value = template_value.replace("֎", "")
                    elif isinstance(template_value, int) and template_key.find("+") != -1:
                        template_key = template_key[:-1]
                        if template_value > 0:
                            template_value = "+" + str(template_value)

                    template.add(template_key, template_value)
            elif key in converter_maps.item_info_box:
                # Remove the value from the template if it is now irrelevant
                template_key = converter_maps.item_info_box[key]
                if template_key.find("+") != -1:
                    template_key = template_key[:-1]
                    if template.has(template_key):
                        template.remove(template_key)


        if 'skin' in item_data and item_data['skin'] != None and item_data['skin'] != "":
            template.add('material', 'Custom')

        # Sprite management
        if item_data['category'] == 'weapon' and not template.has('image'):
            template.add('image', "{{{{WeaponIcon| {} }}}}".format(item_data['type']))

class IdentificationModifier(TemplateModifierBase):
    def update_template(self, template):
        if ":" in self.current_page.name:
            # Ignore if page is not in the default namespace
            return

        # The name to use for API-requests priorities: api-name (template param) > api-name (infobox template param) > name (infobox template param) > page name
        api_name = None
        if template.has("api_name"):
            api_name = str(template.get("api_name").value.strip())
        else:
            infoboxes = self.current_wikitext.filter_templates(matches = "Infobox/(Armour|Item)")
            for ib in infoboxes:
                if ib.has("api_name"):
                    api_name = str(ib.get("api_name").value.strip())
                    break
                elif ib.has("name"):
                    api_name = str(ib.get("name").value.strip())
                    break
            if api_name == None:
                api_name  = self.current_page.name

        items_list = wynn.item.search_item(name=api_name)
        if items_list == None:
            print("No API data was found for the item with the API name '{}' on the page '{}' (Nothing on search)".format(api_name, self.current_page.name))
            return
        item_data = None
        for current_item in items_list:
            if ('displayName' in current_item and current_item.displayName == api_name) or current_item.name == api_name:
                item_data = current_item
                break
        if item_data == None:
            print("No API data was found for the item with the API name '{}' on the page '{}' (Not found in search)".format(api_name, self.current_page.name))
            return

        # Swap to the Identification/Preset if the item is pre-identified
        if 'identified' in item_data and item_data.identified:
            print("The item '{}' on the page '{}' was using the incorrect identification template, fixing it now".format(self.current_page.name, api_name))
            template.name = 'Identification/Preset'
            IdentificationPresetModifier.update_template(self, template)
            return

        # Construction of new template data
        for key in item_data._data:
            if item_data[key] and item_data[key] != None and item_data[key] != 0:
                if key in converter_maps.v1_to_wiki:
                    template_key = converter_maps.v1_to_wiki[key]
                    average_value = item_data[key]
                    if template_key.find("-") != -1:
                        template_key = template_key[:-1]
                        if average_value > 0:
                            value = "+" + str(average_value)
                        else:
                            value = str(average_value)

                        template.add(template_key, value)
                        continue
                    elif average_value > 0:
                        min_value = "+" + str(max(1, round(average_value * 0.3)))
                        max_value = "+" + str(max(1, round(average_value * 1.3)))
                    else:
                        min_value = str(min(-1, round(average_value * 0.7)))
                        max_value = str(min(-1, round(average_value * 1.3)))

                    template.add(template_key, min_value + "/" + max_value)
            elif key in converter_maps.v1_to_wiki:
                # Remove the value from the template if it is now irrelevant
                template_key = converter_maps.v1_to_wiki[key]
                if template.has(template_key):
                    template.remove(template_key)

class IdentificationPresetModifier(TemplateModifierBase):
    def update_template(self, template):
        if ":" in self.current_page.name:
            # Ignore if page is not in the default namespace
            return

        # The name to use for API-requests priorities: api-name (template param) > api-name (infobox template param) > name (infobox template param) > page name
        api_name = None
        if template.has("api_name"):
            api_name = str(template.get("api_name").value.strip())
        else:
            infoboxes = self.current_wikitext.filter_templates(matches = "Infobox/(Armour|Item)")
            for ib in infoboxes:
                if ib.has("api_name"):
                    api_name = str(ib.get("api_name").value.strip())
                    break
                elif ib.has("name"):
                    api_name = str(ib.get("name").value.strip())
                    break
            if api_name == None:
                api_name  = self.current_page.name

        items_list = wynn.item.search_item(name=api_name)
        if items_list == None:
            print("No API data was found for the item with the API name '{}' on the page '{}' (Nothing on search)".format(api_name, self.current_page.name))
            return
        item_data = None
        for current_item in items_list:
            if ('displayName' in current_item and current_item.displayName == api_name) or current_item.name == api_name:
                item_data = current_item
                break
        if item_data == None:
            print("No API data was found for the item with the API name '{}' on the page '{}' (Not found in search)".format(api_name, self.current_page.name))
            return

        # Swap to the Identification if the item is not pre-identified
        if 'identified' not in item_data or ('identified' in item_data and not item_data.identified):
            print("The item '{}' on the page '{}' was using the incorrect identification template, fixing it now".format(self.current_page.name, api_name))
            template.name = 'Identification'
            IdentificationModifier.update_template(self, template)
            return

        # Construction of new template data
        for key in item_data._data:
            if item_data[key] and item_data[key] != None and item_data[key] != 0:
                if key in converter_maps.v1_to_wiki:
                    template_key = converter_maps.v1_to_wiki[key]
                    average_value = item_data[key]
                    if template_key.find("-") != -1:
                        template_key = template_key[:-1]

                    if average_value > 0:
                        average_value = "+" + str(average_value)

                    template.add(template_key, average_value)
            elif key in converter_maps.v1_to_wiki:
                # Remove the value from the template if it is now irrelevant
                template_key = converter_maps.v1_to_wiki[key]
                if template.has(template_key):
                    template.remove(template_key)


print("Connecting to Wynncraft Wiki...")
credentials = AuthCredentials(user_file="me")
wiki = GamepediaClient('wynncraft', credentials=credentials)
print("Connected!")

if len(sys.argv[1:]) > 0:
    # Template Modifier for [[Template:Identification]]
    IdentificationModifier(wiki, 'Identification', summary='Bot edit, update identification template', title_list=sys.argv[1:]).run()
    # Template Modifier for [[Template:Identification/Preset]]
    IdentificationPresetModifier(wiki, 'Identification/Preset', summary='Bot edit, update identification template', title_list=sys.argv[1:]).run()
    # Template Modifier for [[Template:Infobox/Weapon]]
    InfoboxModifier(wiki, 'Infobox/Weapon', summary='Bot edit, update Weapon infobox template', title_list=sys.argv[1:]).run()
    # Template Modifier for [[Template:Infobox/Armour]]
    InfoboxModifier(wiki, 'Infobox/Armour', summary='Bot edit, update Armor infobox template', title_list=sys.argv[1:]).run()
else:
    # Template Modifier for [[Template:Identification]]
    IdentificationModifier(wiki, 'Identification', summary='Bot edit, update identification template').run()
    # Template Modifier for [[Template:Identification/Preset]]
    IdentificationPresetModifier(wiki, 'Identification/Preset', summary='Bot edit, update identification template').run()
    # Template Modifier for [[Template:Infobox/Weapon]]
    InfoboxModifier(wiki, 'Infobox/Weapon', summary='Bot edit, update Weapon infobox template').run()
    # Template Modifier for [[Template:Infobox/Armour]]
    InfoboxModifier(wiki, 'Infobox/Armour', summary='Bot edit, update Armor infobox template').run()