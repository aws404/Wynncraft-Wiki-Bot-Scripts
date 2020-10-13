# Wynncraft Wiki Bot Scripts
This is a collection of scripts that can be used to maintain the Wynncraft Wiki (https://wynncraft.gamepedia.com)

## Required Libraries
### wynn.py Wynncraft API Wrapper
* Link: https://github.com/Zakru/wynn.py
* Install Command: `pip install -U git+git://github.com/Zakru/wynn.py`

### River's Gamepedia API Wrapper 
* Link: https://github.com/RheingoldRiver/river_mwclient) 
* Install Command: `pip install -U git+git://github.com/RheingoldRiver/river_mwclient`

### Python Requests Library
* Install Command: `pip install requests`

## Setup
The following files in **the same directory as your code**:
* `username_me.txt` - your user name for example, `RheingoldRiver@Python`
* `password_me.txt` - your bot password this will be a long string of characters from Special:BotPasswords

## Scripts
### `Ingredients.py`
This script is used to update the templates 'Template:Infobox/Ingredient' and 'Template:Crafting', using data from the Offical Wynncraft API.
#### Example
If no arguments are supplied, the script will update all instanced of the template, for example:  
```
python ingredients.py
```  
A set of one or more pages can also be specified to update, for example:  
```
python ingredients.py Rotten_Flesh Grook_Feather Corrupted_Fragment
```  