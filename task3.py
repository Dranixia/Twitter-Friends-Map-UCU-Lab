import json
from opencage.geocoder import OpenCageGeocode
import folium
import urllib.request
import urllib.parse
import urllib.error
import json
import ssl
import twurl


def irl_processes():
    """
    (None) -> str
    Ignore SSL certificate errors and return data from web page.
    """
    twitter_url = 'https://api.twitter.com/1.1/friends/list.json'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    acct = input('Enter Twitter Account:')
    if len(acct) < 1:
        return 'INVALID ACCOUNT'
    url = twurl.augment(twitter_url,
                        {'screen_name': acct, 'count': '75'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    return data


def dict_receive(script):

    script = json.loads(script)

    user_info = dict()

    for dct in script['users']:
        for key in dct:
            name = dct['name']
            loc = dct['location']
            user_info[name] = loc
    return user_info


def geo_loc(data):
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
    folium_map(geo_loc(dict_receive(irl_processes())))


if __name__ == "__main__":
    main()
