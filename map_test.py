import shapefile
import os, json, xmltodict
import matplotlib.colors as matcolor
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import numpy as np
import load_data as ld
import time

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
    Lat = cwb_data["earthquake"]["epicenter"]["epicenterLat"]["#text"]
    Lon = cwb_data["earthquake"]["epicenter"]["epicenterLon"]["#text"]
    Depth = cwb_data["earthquake"]["depth"]["#text"]
    Magnitude = cwb_data["earthquake"]["magnitude"]["magnitudeValue"]
    pgaAdj = cwb_data["earthquake"]["pgaAdj"]
    print(Lon, Lat)

sf_county = os.path.join(os.path.join(os.getcwd(), "shapefile"),"COUNTY_MOI_1090820")
sf_town = os.path.join(os.path.join(os.getcwd(), "shapefile"),"TOWN_MOI_1091016")

#sf = shapefile.Reader(sf_path+".shp")
#print(sf.fields)


fig = plt.figure()
ax = fig.add_subplot(111)

#for shape in sf.shapeRecords():
#        # end index of each components of map
#    l = shape.shape.parts
#    
#    len_l = len(l)  # how many parts of countries i.e. land and islands
#    x = [i[0] for i in shape.shape.points[:]] # list of latitude
#    y = [i[1] for i in shape.shape.points[:]] # list of longitude
#    l.append(len(x)) # ensure the closure of the last component
#    for k in range(len_l):
        # draw each component of map.
        # l[k] to l[k + 1] is the range of points that make this component
#        plt.plot(x[l[k]:l[k + 1]],y[l[k]:l[k + 1]], 'k-')

map = Basemap(projection = "tmerc", lat_0 = 35, lon_0 = 118,
llcrnrlon = 118, llcrnrlat = 21.5,
urcrnrlon = 123, urcrnrlat = 27,
resolution = "i")

#cb = ["#DCDCDC", "#00FF00", "#FFFF00", "#FF7F50", "FF4500", "#B22222", "#8B0000", "#663399", "#BA55D3"]
#cl = ["1", "2", "3", "4", "5-", "5+", "6-", "6+", "7"]
#cb = matcolor.ListedColormap(cb)
#cl = matcolor.BoundaryNorm(cl, 9)
#cbar = plt.colorbar(orientation='vertical',ticks=cl,shrink=0.4,aspect=25)
#cbar.ax.set_xlabel(xlabel='震度', fontsize=8)

#map.contourf(120,22,cmap=cb,norm=norm,levels=cl,linestyles=None)
map.drawmapboundary(fill_color = "#87CEFA")
#map.fillcontinents(color = "#DCDCDC")
#map.drawcoastlines(linewidth=2.0)

#Draw earthquake center
eqLon, eqLat = map(Lon, Lat)
map.plot(eqLon, eqLat, "*", markersize=12, color="#FFFF00")

patches = []
default_area = []
shape_info = []

map.readshapefile(sf_town, "tw", drawbounds=True, linewidth=0.5)
for i, v in enumerate(map.tw_info):
    print(i, v)
#load data
data = ld.load_data()
for item in data:
    draw_area = {
    "7" : [],
    "6+" : [],
    "6-" : [],
    "5+" : [],
    "5-" : [],
    "4" : [],
    "3" : [],
    "2" : [],
    "1" : [],
    }
    alarm_area = []
    date = item["date"]
    time = item["time"].replace(":",".")
    Area_info = item["Areas"]
    print(date, time)
    for Area_detail in Area_info:
        alarm_area.append(Area_detail)
        #Area_code = Area_detail["AreaCode"]
        #Intensity = Area_detail["Intensity"]
        #Sourece = Area_detail["Source"]
        #PGA = Area_detail["PGA"]
        #print(Area_code)
    alarm_area = sorted(alarm_area, key=lambda k:(k["AreaCode"],k["PGA"]), reverse=True)
    #print(alarm_area)
    for i in alarm_area:
        
        if i["Intensity"] == "1":
            draw_area["1"].append(Polygon(np.array(map.tw[j["SHAPENUM"]])))
        elif i["Intensity"] == "2":
            draw_area["2"].append(Polygon(np.array(map.tw[j["SHAPENUM"]])))
        elif i["Intensity"] == "3":
            draw_area["3"].append(Polygon(np.array(map.tw[j["SHAPENUM"]])))
        elif i["Intensity"] == "4":
            draw_area["4"].append(Polygon(np.array(map.tw[j["SHAPENUM"]])))
        elif i["Intensity"] == "5-":
            draw_area["5-"].append(Polygon(np.array(map.tw[j["SHAPENUM"]])))
        elif i["Intensity"] == "5+":
            draw_area["5+"].append(Polygon(np.array(map.tw[j["SHAPENUM"]])))
        elif i["Intensity"] == "6-":
            draw_area["6-"].append(Polygon(np.array(map.tw[j["SHAPENUM"]])))
        elif i["Intensity"] == "6+":
            draw_area["6+"].append(Polygon(np.array(map.tw[j["SHAPENUM"]])))
        elif i["Intensity"] == "7":
            draw_area["7"].append(Polygon(np.array(map.tw[j["SHAPENUM"]])))

        if i["AreaCode"] == j["TOWNCODE"]:
            shape_loc = j["SHAPENUM"]
                #print(map.tw[shape_loc])
    for key, value in draw_area.items():
        print(key)
        if value != [] and key == "4":
            ax.add_collection(PatchCollection(value, facecolor="#ff0000", edgecolor="k", linewidths=0.5, zorder=2, alpha=0.85))

    plt.title(date+time)
    map.readshapefile(sf_county, "tw_county", drawbounds=True, linewidth=1.5)
    plt.savefig(date+time+".png")
    plt.cla()



#for info, shape in zip(map.tw_info, map.tw):
    #print(info,shape)
    #if info["TOWNCODE"] == "10013040":
        #print(info,shape)
        #patches.append(Polygon(np.array(shape), True))
    #else:
        #default_area.append(Polygon(np.array(shape), True))


#print(type(map.tw))
#print(map.tw[364])
#ar = []
#ar.append(Polygon(np.array(map.tw[364])))
#ax.add_collection(PatchCollection(patches, facecolor="#ff0000", edgecolor="k", linewidths=0.5, zorder=2, alpha=0.85))

#drawing
#ax.add_collection(PatchCollection(patches, facecolor="#B22222", edgecolor="k", linewidths=0.5, zorder=2))
#ax.add_collection(PatchCollection(default_area, facecolor="#DCDCDC", edgecolor="k", linewidths=0.5, zorder=2, alpha=0.85))

        #x, y = zip(*shape)
        #map.plot(x, y, marker = None, color= "m")

# display


#map.grid(True, which='both')

#for i in sf:
#    town_id = int(i['properties']['TOWNCODE'])
#    shapes[town_id] = shape(i['geometry'])
#    properties[town_id] = i['properties']
#    print(town_id, shapes[town_id], properties[town_id])


