import requests as r

def get_ingredient(name):
    """
    Sends GET request to Wynncraft API to get information on ingredient 'name'.
    If the ingredient was not found, returns None
    """
    URL = f'https://api.wynncraft.com/v2/ingredient/get/{name}'.replace(' ', '_')
    res = r.get(URL) # gets the response

    # if no ingredient was found
    if res.status_code == 400: return None
    # return first ingredient found
    return res.json()['data'][0]


def search_item(name):
    """
    Sends GET request to Wynncraft API to get information on item 'name'.
    If the item was not found, returns None
    Else returns list of found items
    """
    URL = f'https://api.wynncraft.com/public_api.php?action=itemDB&search={name}'.replace(' ', '_')
    res = r.get(URL) # gets the response

    res = res.json() # gets the data
    del res['request'] # deletes 'request'

    # if no items were found return None
    if res['items'] == []: return None
    # return first item found
    return res['items']
