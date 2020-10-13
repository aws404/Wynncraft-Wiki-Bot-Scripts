# Wynncraft Wiki Bot Scripts

## Required Libraries
1. 'wynn.py Wynncrfat API Wrapper' (https://github.com/Zakru/wynn.py) - `pip install -U git+git://github.com/Zakru/wynn.py`
2. 'River's Gamepedia API Wrapper' (https://github.com/RheingoldRiver/river_mwclient) - `pip install -U git+git://github.com/RheingoldRiver/river_mwclient`
3. 'Python Requests Library' = `pip install requests`

## Setup
The following files in **the same directory as your code**:
* `username_me.txt` - your user name for example, `RheingoldRiver@Python`
* `password_me.txt` - your bot password this will be a long string of characters from Special:BotPasswords

## Scripts
#### `Ingredients.py`
This script is used to update the templates 'Template:Infobox/Ingredient' and 'Template:Crafting', running it will update all content pages that use these templates.