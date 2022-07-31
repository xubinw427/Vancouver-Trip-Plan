#!/usr/bin/env python
# coding: utf-8
# author: Xubin Wang
# In[4]:


import sys
import pandas as pd
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


# https://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image
def get_exif(fn):
    exif_data = {}
    i = Image.open(fn)
    info = i._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data


def convert_to_degress(value):
    d = value[0]
    m = value[1]
    s = value[2]

    return d + (m / 60.0) + (s / 3600.0)


def get_if_exist(data, key):
    if key in data:
        return data[key]
    return None


def get_lat(data):
    # print(exif_data)
    if 'GPSInfo' in data:
        gps_info = data["GPSInfo"]
        gps_latitude = get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = get_if_exist(gps_info, 'GPSLatitudeRef')
        if gps_latitude and gps_latitude_ref:
            lat = convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat
            lat = str(f"{lat:.{6}f}")
            #                 print(lat)
            return lat
    else:
        return None


def get_lon(data):
    # print(exif_data)
    if 'GPSInfo' in data:
        gps_info = data["GPSInfo"]
        gps_longitude = get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = get_if_exist(gps_info, 'GPSLongitudeRef')
        if gps_longitude and gps_longitude_ref:
            lon = convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon
            lon = str(f"{lon:.{6}f}")
            #                 print(lon)
            return lon
    else:
        return None


# https://stackoverflow.com/questions/63139812/how-to-read-multiple-images-in-python
def read_pics(src):
    files = os.listdir(src)  # Getting the files to copy
    locations = []
    for idx, image_src in enumerate(files):
        if (image_src.endswith('.jpg')):
            a = get_exif(f'{src}{image_src}')
            lat = get_lat(a)
            lon = get_lon(a)
            coordinate = [lat, lon]
            locations.append(coordinate)
    return locations


def main():
    # read coordinates of your pics
    locations = read_pics('pics/')

    # write to file
    data = pd.DataFrame(locations, columns=['lat', 'lon'])
    data.to_csv('data/locations.csv', index=False)


if __name__ == '__main__':
    main()

# In[ ]:
