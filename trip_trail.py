#!/usr/bin/env python
# coding: utf-8
# author: Xubin Wang
# In[1]:


import pandas as pd
import numpy as np
import folium
import copy
from geopy.geocoders import Nominatim
from folium import plugins

# In[2]:


food = ['cafe', 'fast_food', 'bbq', 'restaurant', 'pub', 'bar', 'food_court', 'ice_cream', 'bistro', 'juice_bar',
        'disused:restaurant', 'water_point', 'biergarten']
entertament = ['place_of_worship', 'public_building', 'cinema', 'theatre', 'dojo', 'arts_centre', 'nightclub',
               'stripclub', 'gambling', 'spa', 'watering_place', 'park', 'casino', 'hunting_stand']


def cal_between(points):
    lat1 = points['lat']
    lon1 = points['lon']
    lat2 = points['lat1']
    lon2 = points['lon1']

    R = 6371
    dLat = np.deg2rad(lat2 - lat1)
    dLon = np.deg2rad(lon2 - lon1)
    a = np.sin(dLat / 2) * np.sin(dLat / 2) + np.cos(np.deg2rad(lat1)) * np.cos(np.deg2rad(lat2)) * np.sin(
        dLon / 2) * np.sin(dLon / 2);
    c = 2 * np.arcsin(np.sqrt(a)) * 1000
    return R * c


# https://towardsdatascience.com/reverse-geocoding-in-python-a915acf29eb6
def guess_where_R_U(lat, lon):
    locator = Nominatim(user_agent='myLocator')
    location = str(lat) + ',' + str(lon)
    location = locator.reverse(location)
    name = location.raw['display_name'].split(',')
    return name[0] + "," + name[1] + "," + name[2]


def drow_folium_map(points, vmap):
    for coors in points:
        name = guess_where_R_U(coors[0], coors[1])
        folium.CircleMarker(location=coors,
                            radius=50,
                            popup="<strong>visited place</strong>",
                            icon=folium.Icon(color='blue'),
                            fill=True,
                            fill_color='#3186cc',
                            tooltip=name).add_to(vmap)
    return vmap


def drow_around_facilities(points, vmap):
    for index, row in points.iterrows():
        lat = row['lat']
        lon = row['lon']
        name = row['name']
        if row.amenity in food:
            folium.Marker(location=[lat, lon],
                          popup=name,
                          icon=folium.Icon(color='red'),
                          tooltip=name).add_to(vmap)
        else:
            folium.Marker(location=[lat, lon],
                          popup=name,
                          icon=folium.Icon(color='green'),
                          tooltip=name).add_to(vmap)
    return vmap


def get_around_facilities(coors, vmap, data):
    for i in coors:
        #         print(i)
        tempdata = copy.deepcopy(data)
        tempdata['lat1'] = i[0]
        tempdata['lon1'] = i[1]
        Van = tempdata.apply(cal_between, axis=1)
        idx = Van[Van < 1000]
        #         print(len(idx))
        around_van = tempdata.iloc[idx.index]
        pd_food = around_van[around_van.amenity.isin(food)]
        pd_enter = around_van[around_van.amenity.isin(entertament)]
        vmap = drow_around_facilities(pd_food, vmap)
        vmap = drow_around_facilities(pd_enter, vmap)
    return vmap


# In[5]:


def main():
    Vancouver = [49.282730, -123.120735]
    data = pd.read_json('amenities-vancouver.json.gz', lines=True)
    locations = pd.read_csv('data/locations.csv')
    coors = list(locations.itertuples(index=False, name=None))
    # Initialize Map
    vmap = folium.Map(location=Vancouver, tiles='OpenStreetMap', zoom_start=12)
    # Add The Location of Your Pic to Map
    vmap = drow_folium_map(coors, vmap)
    # Draw Path Between Each picture
    plugins.AntPath(coors).add_to(vmap)
    # Get Food and Entertaments Within 1000 meters.
    vmap = get_around_facilities(coors, vmap, data)

    vmap.save("html/map.html")


if __name__ == '__main__':
    main()

# In[ ]:
