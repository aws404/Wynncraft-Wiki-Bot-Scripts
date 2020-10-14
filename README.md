# Wynncraft Wiki Bot Scripts
This is a collection of scripts that can be used to maintain the Wynncraft Wiki (https://wynncraft.gamepedia.com)

## Required Libraries
### wynn.py Wynncraft API Wrapper
* Link: https://github.com/Zakru/wynn.py
* Install Command: `pip install -U git+git://github.com/Zakru/wynn.py`

### River's Gamepedia API Wrapper 
* Link: https://github.com/RheingoldRiver/river_mwclient  
* Install Command: `pip install -U git+git://github.com/RheingoldRiver/river_mwclient`

### Python Requests Library
* Install Command: `pip install requests`

## Setup
The following files in **the same directory as your code**:
* `username_me.txt` - your user name for example, `RheingoldRiver@Python`
* `password_me.txt` - your bot password this will be a long string of characters from Special:BotPasswords

## Scripts
### `ingredients.py`
This script is used to update all the 'Template:Infobox/Ingredient' and 'Template:Crafting' templates using data from the Offical Wynncraft API.
#### Example
If no arguments are supplied, the script will update all instances of the template, for example:  
```
python ingredients.py
```  
A set of one or more pages can also be specified to update, for example:  
```
python ingredients.py Rotten_Flesh Grook_Feather Corrupted_Fragment
```  

### `items.py`
This script is used to update all the 'Template:Infobox/Armour', 'Template:Infobox/Weapon', 'Template:Identification' and 'Template:Identification/Preset' templates using data from the Offical Wynncraft API.
#### Example
If no arguments are supplied, the script will update all instances of the template, for example:  
```
python items.py
```  
A set of one or more pages can also be specified to update, for example:  
```
python items.py Infused_Hive_Weapons "Bob's_Mythic_Weapons" "Olux's_Prized_Weapons"
```  

### `common.py`
This is not a runnable script, it is a collection of common functions and tools that are used in multiple scripts

### `converter_maps.py`
This is not a runnable script, it is a collection of dictionaries used to convert various values from API names to wiki template names