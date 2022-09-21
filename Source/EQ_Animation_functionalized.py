#!/usr/bin/env python
# coding: utf-8

# In[95]:


import geopandas as gpd
import pandas as pd
import os, json, xmltodict, math
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
import load_data_new_type as ld
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path
#from IPython import get_ipython
#get_ipython().run_line_magic('matplotlib', 'inline')
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import imageio


# In[100]:


class Animation():
    def __init__(self, chooseEvent, fps=10, dpi=80):
        # Basic Setting
        self.root_path = os.path.normpath("C:\\Git\\eqreplay")
        self.shapefile_path = os.path.join(self.root_path, "Source\\Shapefile")
        self.data_folder = os.path.join(self.root_path, "Data", chooseEvent)
        self.dpi = dpi
        self.init = True
        # Vars
        self.trigger_site = []
        self.trigger_cwb = []
        self.calculating_list = []
        self.data_list = []
        self.sp_site = ["S00049"]

        self.frame_rate = fps         #10 frame/per second
        self.s_radius = 0.045 
        self.p_radius = 0.055   
        


        #zero point
        self.origin_x = 119
        self.origin_y = 21.8
        self.delta_x = 3.3
        self.delta_y = 3.7

        self.t_size = 20 #text size

        self.cbw = 2.3 #county_boundary_width
        self.tbw = 0.5 #town_boundary_width
        
        # do init
        self.loadfile()
        self.CWBconfig() ## Load CWB and speed config
        self.loadshapefile()
        self.loaddatafile()
        
        self.colormapconfig()
        print(self.replay_start_time, self.site_geo.iloc[-1]["Trigger_Time"]+timedelta(seconds=1))
        #output config
        self.Image_path = os.path.join(self.root_path, "Output\\Images\\"+self.Identifier)
        self.Gif_path = os.path.join(self.root_path, "Output\\Gifs\\"+self.Identifier)
        Path(self.Image_path).mkdir(parents=True, exist_ok=True)
        Path(self.Gif_path).mkdir(parents=True, exist_ok=True)
        
    def loadfile(self):
        for root, dirs, files in os.walk(self.data_folder):
            for file in files:
                try:
                    if file.startswith("CWB"):
                        self.CWB_file = os.path.join(root, file)
                        #print(self.CWB_file)
                    elif file.endswith('Alarm.json'):
                        self.Alarm_file = os.path.join(root, file)
                        #print(self.Alarm_file)               
                    elif file.endswith('Site.json'):
                        self.Site_file = os.path.join(root, file)
                except AttributeError as e:
                    print(e)
                    return '1'
                    
    def CWBconfig(self):
        try:
            if self.CWB_file.endswith('xml'):
                with open(self.CWB_file, encoding="utf-8") as xml_file:
                    data_dict = xmltodict.parse(xml_file.read())
                    cwb_data = json.loads(json.dumps(data_dict, ensure_ascii=False).encode("utf-8").decode())
                    self.Identifier = cwb_data["earthquake"]["identifier"]
                    self.SchemaVer = cwb_data["earthquake"]["schemaVer"]
                    self.Language = cwb_data["earthquake"]["language"]
                    self.SenderName = cwb_data["earthquake"]["senderName"]
                    self.SentTime = cwb_data["earthquake"]["sent"]
                    self.Status = cwb_data["earthquake"]["status"]
                    self.Msgtype = cwb_data["earthquake"]["msgType"]
                    self.MsgNo = cwb_data["earthquake"]["msgNo"]
                    self.Description = cwb_data["earthquake"]["description"]
                    Origintime = cwb_data["earthquake"]["originTime"]
                    self.Lat = float(cwb_data["earthquake"]["epicenter"]["epicenterLat"]["#text"])
                    self.Lon = float(cwb_data["earthquake"]["epicenter"]["epicenterLon"]["#text"])
                    self.Depth = cwb_data["earthquake"]["depth"]["#text"]
                    self.Magnitude = cwb_data["earthquake"]["magnitude"]["magnitudeValue"]
                    self.pgaAdj = cwb_data["earthquake"]["pgaAdj"]

                    self.cwb_origin_time = datetime.strptime(Origintime.replace("T", " "), "%Y-%m-%d %H:%M:%S+08:00").timestamp() 
                    self.replay_start_time = datetime.strptime(Origintime.replace("T", " "), "%Y-%m-%d %H:%M:%S+08:00").timestamp() - 3
                    #print(replay_start_time, cwb_origin_time)
                    #print(datetime.fromtimestamp(replay_start_time))
            elif self.CWB_file.endswith("txt"):
                with open(self.CWB_file, encoding="utf-8") as file:
                    cwb_data = json.loads(file.read())
                    self.Identifier = cwb_data.get("Identifier", None)
                    self.SchemaVer = cwb_data.get("SchemaVer", None)
                    self.Language = cwb_data.get("Language", None)
                    self.SenderName = cwb_data.get("SenderName", None)
                    self.SentTime = cwb_data.get("Sent", None)
                    self.Status = cwb_data.get("Status", None)
                    self.Msgtype = cwb_data.get("MsgType", None)
                    self.MsgNo = cwb_data.get("MsgNo", None)
                    self.Description = cwb_data.get("Description", None)
                    Origintime = cwb_data.get("OriginTime", None)
                    self.Lat = float(cwb_data.get("EpiCenterLat", None))
                    self.Lon = float(cwb_data.get("EpiCenterLon", None))
                    self.Depth = cwb_data.get("Depth", None)
                    self.Magnitude = cwb_data.get("Depth", None)
                    self.pgaAdj = cwb_data.get("PgaAdj", None)
                    
                    self.cwb_origin_time = datetime.strptime(Origintime.replace("T", " "), "%Y-%m-%d %H:%M:%S+08:00").timestamp() 
                    self.replay_start_time = datetime.strptime(Origintime.replace("T", " "), "%Y-%m-%d %H:%M:%S+08:00").timestamp() - 3
                    
            ## Set Swave and pwave speed by Depth
            if 30.0 >= float(self.Depth) > 0 :
                #10.0Km
                self.s_speed = 0.0023
                self.p_speed = 0.0048
            elif 60.0 >= float(self.Depth) > 30.0:
                #20.0Km
                self.s_speed = 0.0021
                self.p_speed = 0.0046
            elif 90.0 >= float(self.Depth) > 30.0:
                #20.0Km
                self.s_speed = 0.0019
                self.p_speed = 0.0044
            elif 120.0 >= float(self.Depth) > 90.0:
                #20.0Km
                self.s_speed = 0.0017
                self.p_speed = 0.0042
            
        except Exception as e:
            print(e)
            return 'CWB Error'
    
    def colormapconfig(self):
        # Color Bar color setting
        self.color_map = [
                '#C4FBE2',
                '#26FF0B',
                '#FFFE0B',
                '#FF810B',
                '#FF550B',
                '#AC1F14',
                '#b834bf',
                '#cc6eff',
                #'#BB20D9'
        ]
        self.cLevel = [1, 2, 3, 4, 5, 5.5, 6, 6.5, 7]
        self.cmap, self.norm = matplotlib.colors.from_levels_and_colors(self.cLevel, self.color_map)#, extend="max")
    
    def mapinit(self):
        #map init
        f, self.axes = plt.subplots(figsize=(700/self.dpi, 760/self.dpi))
        #print(type(f), type(self.axes))
        
        f.tight_layout(rect=[-0.01, 0, 1, 0.98]) #rect=[0(左), 0.03(下), 1(右), 0.95(上)]
        #plt.subplots_adjust(left=0, bottom=0, right=0.1/self.dpi, top=0.1/self.dpi, wspace=0, hspace=0)
        
        axes_cb = inset_axes(self.axes,
                        width="3%",  # width = 50% of parent_bbox width
                        height="30%",  # height : 5%
                        loc='lower right')

        f.colorbar(matplotlib.cm.ScalarMappable(norm=self.norm, cmap=self.cmap), cax=axes_cb, ax=self.axes, orientation='vertical', label='Intensity')

        self.axes.set_title(self.Identifier, fontsize=25)
        self.county.boundary.plot(ax=self.axes, color="black", edgecolor="black",linewidth=self.cbw, zorder=2)  #draw counties
        self.l1 = self.town.plot(ax=self.axes, color="#dddddd", edgecolor="black", linewidth=self.tbw, zorder=1)     #draw towns

        #set pic location
        minx, miny, maxx, maxy = (self.origin_x, self.origin_y, self.origin_x + self.delta_x, self.origin_y + self.delta_y)
        self.l1.set_xlim(minx, maxx)
        self.l1.set_ylim(miny, maxy)
        #event_time = (datetime.strptime(Origintime.replace("T", " "), "%Y-%m-%d %H:%M:%S+08:00"))
        self.replay_time = datetime.fromtimestamp(self.replay_start_time)

        #TextBoxes
        self.axes_time = self.axes.text(minx+0.1, maxy-0.1, self.replay_time, size=self.t_size)
        self.axes_site_count = self.axes.text(119.5, 24.7, "#Sites: "+str(len(self.trigger_site)), size=self.t_size, style='italic', c="gray")
        self.axes_cwb_count = self.axes.text(119.5, 24.6, "#CWB: "+str(len(self.trigger_cwb)), size=self.t_size, style='italic', c="gray")


        #plotting eq_center
        self.eq_center = pd.DataFrame({"Name":"eq_center", "Latitude":[self.Lat], "Longitude":[self.Lon]})
        self.eq_center = gpd.GeoDataFrame(self.eq_center, geometry=gpd.points_from_xy(self.eq_center.Longitude, self.eq_center.Latitude))
        self.eq_center.plot(ax=self.axes, color="#00ffaa", marker="*", markersize=1000, zorder=3)

        #before_event_process
        while self.replay_time <= datetime.fromtimestamp(self.cwb_origin_time):
            self.replay_time += timedelta(seconds=(1/self.frame_rate))
            print(self.replay_time)
            self.replay_time_str = self.replay_time.strftime("%Y-%m-%d %H_%M_%S.%f")[:-5]
            self.axes.texts[-3].set_text((self.replay_time_str.replace("_",":")+ "({})".format(round(self.replay_time.timestamp() - self.cwb_origin_time ,2))))
            self.axes.plot()
            self.axes.figure.savefig(self.Image_path+"\\"+self.replay_time_str+".png", dpi=self.dpi)

        self.data_index = 0
    
    def loadshapefile(self):
        try:
            self.town = gpd.read_file(self.shapefile_path+"\TOWN_MOI_1091016.shp", encoding="utf-8")
            self.county = gpd.read_file(self.shapefile_path+"\COUNTY_MOI_1090820.shp", encoding="utf-8")
            self.crs = self.county.crs
        except Exception as e:
            return 'loadshapefile Error'
    def loaddatafile(self):
        try:
        
            # MQTT Data
            self.data = ld.load_data(self.Alarm_file)
            self.replay_end_time = datetime.strptime(self.data[-1]["Date"]+" "+self.data[-1]["Time"], "%Y-%m-%d %H:%M:%S.%f").timestamp() #data.iloc[-1, 0].timestamp()
            self.replay_loop = round((self.replay_end_time-self.replay_start_time)/(1/self.frame_rate))
            
            # SITE Data
            self.site_df = ld.load_site(self.Site_file)
            self.site_df["Calculate_Time"] = ""
            #print(self.site_df)

            for index, row in self.site_df.iterrows():
                if row["Site_ID"] in self.sp_site:
                    time_tmp = row["Trigger_Time"] - timedelta(seconds=1)
                    self.site_df.iloc[index, self.site_df.columns.get_loc("Calculate_Time")] = time_tmp

                else:
                    time_tmp = row["Trigger_Time"] - timedelta(seconds=3)
                    self.site_df.iloc[index, self.site_df.columns.get_loc("Calculate_Time")] = time_tmp
            #print(self.site_df)
            self.site_geo = gpd.GeoDataFrame(self.site_df, geometry=gpd.points_from_xy(self.site_df.Site_Lon, self.site_df.Site_Lat))
            #print(self.site_geo)
        except Exception as e:
            print(e)
            return 'loaddatafile Error'
        
    def draw(self):
        self.mapinit()
        for time in range(self.replay_loop):

            #Main loop使用到的變數
            AreaDetail = []
            draw_area = gpd.GeoDataFrame()
            self.replay_time_str = self.replay_time.strftime("%Y-%m-%d %H_%M_%S.%f")[:-5]
            #print(replay_time)

            #P波、S波的初始化
            self.p_circle = plt.Circle((self.Lon, self.Lat), radius=self.p_radius, color="red", lw=2.0, ls="--", fill=False)
            self.axes.add_patch(self.p_circle)
            self.s_circle = plt.Circle((self.Lon, self.Lat), radius=self.s_radius, color="red", lw=2.0, fill=False)
            self.axes.add_patch(self.s_circle)

            #繪製計算中站台
            calculating_site = self.site_geo.loc[self.replay_time >= self.site_geo["Calculate_Time"]]
            for index, row in self.site_geo.iterrows():

                #若播放時間大於站台計算時間
                if self.replay_time >= row["Calculate_Time"]:
                    if row["Site_ID"] not in self.calculating_list:
                        self.calculating_list.append(row["Site_ID"])                
                        calculating_site_plot = self.site_geo.iloc[[index], :]
                        #print(calculating_site_plot)
                        calculating_site_plot.plot(ax=self.axes, color="#3BFF3A", marker=7, markersize=250, zorder=3)#, edgecolor="black"
                        #axes.figure.savefig(str(time)+"C"+".png")


                #若播放時間大於站台觸發時間
                if self.replay_time >= row["Trigger_Time"] and row["Site_ID"] in self.calculating_list:
                    if row["Site_ID"] not in self.trigger_site:
                        self.trigger_site.append(row["Site_ID"])
                        trigger_site_plot = self.site_geo.iloc[[index], :]
                        trigger_site_plot.plot(ax=self.axes, color="#FFFB00", marker=7, markersize=250, zorder=3)#, edgecolor="black"
                        self.axes.texts[-2].set_text("#Sites: "+str(len(self.trigger_site)))

            #若播放時間大於現地預警時間
            if self.replay_time >= datetime.strptime(self.data[self.data_index]["Date"]+" "+self.data[self.data_index]["Time"], "%Y-%m-%d %H:%M:%S.%f"):
                #print("plot data")

                Areas = self.data[self.data_index]["Areas"]
                for Area in Areas:
                    AreaDetail.append((Area["AreaCode"], Area["Source"], Area["PGAx"], ld.pga_to_level(float(Area["PGAx"]))))
                    if Area["Source"] not in self.trigger_cwb and Area["Source"].startswith("CWB"):
                        self.trigger_cwb.append(Area["Source"])
                        self.axes.texts[-1].set_text("#CWB: "+str(len(self.trigger_cwb)))

                Area_df = pd.DataFrame(AreaDetail, columns=["AreaCode", "Source", "PGA", "Intensity"])
                Area_df = Area_df.sort_values(by=["AreaCode", "PGA"])
                for i in range(len(Area_df)):
                    draw = self.town[self.town.TOWNCODE == Area_df.loc[i, "AreaCode"]]
                    draw = draw.assign(Intensity = Area_df.loc[i, "Intensity"])
                    draw_area = draw_area.append(draw)

                #print(draw_area)
                draw_area.plot("Intensity", ax=self.axes, cmap=self.cmap, norm=self.norm)

                self.data_index += 1

            #P波、S波及字串處理
            ##1.P波、S波的累加
            self.p_radius += self.p_speed*self.frame_rate*(1/self.frame_rate)
            self.s_radius += self.s_speed*self.frame_rate*(1/self.frame_rate)
            ##2.時間字串處理
            self.axes.texts[-3].set_text((self.replay_time_str.replace("_",":")+ "({})".format(round(self.replay_time.timestamp() - self.cwb_origin_time ,2))))

            self.axes.plot()
            self.axes.figure.savefig(self.Image_path+"/"+self.replay_time_str + ".png", dpi=self.dpi)

            
            #回放時間超過最後觸發站台則停止
            print(self.replay_time)
            if self.replay_time > self.site_geo.iloc[-1]["Trigger_Time"]+timedelta(seconds=1):
                break

            #儲存後的動作
            self.p_circle.remove()
            self.s_circle.remove()
            self.replay_time += timedelta(seconds=(1/self.frame_rate))
            
    def creategif(self):
        impath = self.Image_path
        filenames = os.listdir(impath)
        img = []
        for filename in filenames:
            #print(filename)
            img.append(imageio.imread(os.path.join(impath, filename)))
        print("張數:",len(img))
        imageio.mimsave(os.path.join(self.Gif_path, self.Identifier+".gif"), img, fps=self.frame_rate)


# In[101]:


#draw = Animation('2022_09_18', 10, 80)
#draw.draw()


# In[102]:


#draw.creategif()


# In[ ]:




