Project Topic: OSM, Photos, and Tours

Team member:  Xiaohang Hu, Yangxin Ma, Xubin Wang

Libraries:
import sys
import pandas as pd
import os
from PIL import Image                  # using pip install PIL
from PIL.ExifTags import TAGS, GPSTAGS
import folium                          # using pip install folium
import copy
from geopy.geocoders import Nominatim  #using pip install geopy
from folium import plugins
from folium.plugins import MarkerCluster
import seaborn
Work Done By Xubin Wang: Get Photos, Form Trip Route and City Analyze
1. Read EXIF data from images
	Run python3 read_pic.py 
2. Draw route of your walk and find food and entertaments around
    Run python3 trip_trail.py
3. Analize data of Cities
    Run python3 analize_city.py
Work Done By Yangxin Ma:

Work Done By Xiaohang Hu:
    