#!/usr/bin/env python
# coding: utf-8

# In[472]:


import geopandas as gpd
import pandas as pd
import os, json, xmltodict
import matplotlib.pyplot as plt
import matplotlib
import load_data as ld
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LinearSegmentedColormap
get_ipython().run_line_magic('matplotlib', 'inline')


# In[473]:


shapefile_path = os.path.join(os.getcwd(), "shapefile")

#cwbxml
with open(os.getcwd()+"\\xml\\cwb.xml", encoding="utf-8") as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    cwb_data = json.loads(json.dumps(data_dict, ensure_ascii=False).encode("utf-8").decode())
    Identifier = cwb_data["earthquake"]["identifier"]
    Schemaver = cwb_data["earthquake"]["schemaVer"]
    Language = cwb_data["earthquake"]["language"]
    Sendername = cwb_data["earthquake"]["senderName"]
    Senttime = cwb_data["earthquake"]["sent"]
    Status = cwb_data["earthquake"]["status"]
    Msgtype = cwb_data["earthquake"]["msgType"]
    MsgNo = cwb_data["earthquake"]["msgNo"]
    Description = cwb_data["earthquake"]["description"]
    Origintime = cwb_data["earthquake"]["originTime"]
    Lat = float(cwb_data["earthquake"]["epicenter"]["epicenterLat"]["#text"])
    Lon = float(cwb_data["earthquake"]["epicenter"]["epicenterLon"]["#text"])
    Depth = cwb_data["earthquake"]["depth"]["#text"]
    Magnitude = cwb_data["earthquake"]["magnitude"]["magnitudeValue"]
    pgaAdj = cwb_data["earthquake"]["pgaAdj"]
    


# In[474]:


town = gpd.read_file(shapefile_path+"\TOWN_MOI_1091016.shp", encoding="utf-8")
county = gpd.read_file(shapefile_path+"\COUNTY_MOI_1090820.shp", encoding="utf-8")
crs = county.crs


# In[475]:


#plotting eq data
color_map = [
        '#f3f3f3',
        '#1aff1a',
        '#ffff00',
        '#ff8900',
        '#ff5500',
        '#b64100',
        '#993300',
        '#aa3c00',
        '#800080'
]
cLevel = [1, 2, 3, 4, 5, 5.5, 6, 6.5, 7]
cmap, norm = matplotlib.colors.from_levels_and_colors(cLevel, color_map, extend="max")

#norm = matplotlib.colors.BoundaryNorm(cLevel,9)
#norm = matplotlib.colors.Normalize(vmin=1, vmax=7, clip=True)
#cm = matplotlib.colors.ListedColormap(color_map)
#cmap1 = LinearSegmentedColormap.from_list("my_colormap", color_map, N=9, gamma=1.0)


#eq_data
data = ld.load_data()

for item in data:
    #map init
    f, axes = plt.subplots(figsize=(15,15))
    county.boundary.plot(ax=axes, color="black", edgecolor="black",linewidth=2, zorder=2)
    l1 = town.plot(ax=axes, color="#dddddd", edgecolor="black", linewidth=0.8, zorder=1)

    #set pic location
    minx, miny, maxx, maxy = (119, 21.8, 122.3, 25.5)
    l1.set_xlim(minx, maxx)
    l1.set_ylim(miny, maxy)

    #plotting eq_center
    eq_center = pd.DataFrame({"Name":"eq_center", "Latitude":[Lat], "Longitude":[Lon]})
    eq_center = gpd.GeoDataFrame(eq_center, geometry=gpd.points_from_xy(eq_center.Longitude, eq_center.Latitude))
    eq_center.plot(ax=axes, color="#00ffaa", marker="*", markersize=1000, zorder=3)
    
    
    date = item["date"]
    time = item["time"]
    Areas = item["Areas"]
    AreaDetail = []
    draw_area = gpd.GeoDataFrame()
    print(date,time)
    
    #plotting
    for Area in Areas:
        AreaDetail.append((Area["AreaCode"], Area["Source"], Area["PGA"], float(Area["Intensity"])))
        
    data = pd.DataFrame(AreaDetail, columns=["AreaCode", "Source", "PGA", "Intensity"])
    data = data.sort_values(by=["AreaCode", "PGA"])
    for i in range(len(data)):
        draw = town[town.TOWNCODE == data.loc[i, "AreaCode"]]
        draw = draw.assign(Intensity = data.loc[i, "Intensity"])
        draw_area = draw_area.append(draw)

    draw_area.plot("Intensity", ax=axes, cmap=cmap, norm=norm, legend=True)