"""
Butynets' Danylo
"""


from opencage.geocoder import OpenCageGeocode
import folium
import urllib.request
import urllib.parse
import urllib.error
import json
import ssl
import twurl


def url_processes():
    """
    (None) -> str
    Ignore SSL certificate errors and return data from twitter page.
    """
    twitter_url = 'https://api.twitter.com/1.1/friends/list.json'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    acct = input('Enter Twitter Account:')
    if len(acct) < 1 or ' ' in acct:
        return 'INVALID ACCOUNT'
    url = twurl.augment(twitter_url,
                        {'screen_name': acct, 'count': '75'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    return data


def dict_receive(script):
    """
    (str) -> dict
    Return the dict with friend users and their locations from json formatted string.
    """
    script = json.loads(script)

    user_info = dict()

    for dct in script['users']:
        for key in dct:
            name = dct['screen_name']
            loc = dct['location']
            user_info[name] = loc
    return user_info


def geo_loc(data):
    """
    (dict) -> dict
    Return dict with users and their location coordinates using OpenCage.
    """
    locs = dict()

    code = '03b39cb989ef458aa9ed842df41b6d40'
    geo_coder = OpenCageGeocode(code)
    for key in data:
        try:
            result = geo_coder.geocode(data[key], no_annotations='1')
            if result and len(result):
                longitude = result[0]['geometry']['lng']
                latitude = result[0]['geometry']['lat']
                locs[key] = (latitude, longitude)
            else:
                continue
        except:
            continue
    return locs


def folium_map(info):
    """
    (dict) ->  None
    """
    html_map = folium.Map(location=[0, 0],
                          zoom_start=4)
    user_layer = folium.FeatureGroup('locations')
    for key in info:
        user_layer.add_child(folium.Marker(location=info[key],
                                           popup=key,
                                           icon=folium.Icon(color='red',
                                                            icon='info-sign')))
    html_map.add_child(user_layer)
    html_map.add_child(folium.LayerControl())
    html_map.save("map.html")


def main():
    name = url_processes()
    if name != 'INVALID ACCOUNT':
        folium_map(geo_loc(dict_receive(name)))

if __name__ == "__main__":
    main()
