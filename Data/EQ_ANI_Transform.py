import os
import sys
import json
import math
import pathlib
class dataTransfer():
    
    
    def siteData(filename, filepath, savefolder):
        path = os.path.normpath(filepath)
        savepath = os.path.normpath(os.path.join(savefolder, "Trans_"+filename))
        msg = {
            "Date":None,
            "Time":None,
            "Site_ID":None,
            "PGAx":None
        }
        arr = []
        with open(path, 'r') as f:
            data = f.readlines()
            for li in data:
                line = json.loads(li)
                Date = line["EventTime"].split(" ")[0].replace("/", "-")
                Time = line["EventTime"].split(" ")[1]
                msg["Date"] = Date
                msg["Time"] = Time
                msg["Site_ID"] = line["SiteID"]
                msg["PGAx"] = line["PGAx"]
                if float(msg["PGAx"]) != 0:
                    #print(msg)
                    arr.append(msg.copy())
        with open(savepath, "w") as w:
            w.write(json.dumps(arr))
        
    
    def alarmData(filename, filepath, savefolder):
        path = os.path.normpath(filepath)
        savepath = os.path.normpath(os.path.join(savefolder, "Trans_"+filename))
        msg = {
            "Date":None,
            "Time":None,
            "Areas":[]
        }
    # try:
        with open(path, 'r') as f:
            data = f.readlines()
            #print(data)
            arr = []
            for li in data:
                msg["Areas"] = []
                line = json.loads(li)
                MsgType = line["Type"]
                if MsgType == "Exercise" or MsgType == "Test":
                    continue
                areaList = line["AreaList"]
                Date = line["SendTime"].split(" ")[0]
                Time = line["SendTime"].split(" ")[1]
                msg["Date"] = Date
                msg["Time"] = Time
                for i in areaList:
                    detail = {
                        "AreaCode":None,
                        "Source":None,
                        "PGAx":None
                    }
                    detail["AreaCode"] = i["AreaCode"]
                    detail["Source"] = i["Source"]
                    if i["Source"] == "CWB":
                        detail["PGAx"] = round(float(i["PGAx"]), 4)
                    detail["PGAx"] = float(i["PGAx"])
                    msg["Areas"].append(detail)
                arr.append(msg.copy()) ### Weired situation check https://stackoverflow.com/questions/65397792/append-a-dictionary-in-a-list-with-loop-very-very-weird

            with open(savepath, "w") as w:
                w.write(json.dumps(arr))
                # with open(savepath, "a+") as w:
                #     w.write(json.dumps(msg))
    # except Exception as e:
    #     print(e)
    #     pass



#dataTransfer.alarmData('Alarm.json','C:\\Git\\eqreplay\\Data\\2022_06_28\\Alarm.json','C:\\Git\\eqreplay\\Data\\2022_06_28\\')
#dataTransfer.siteData('Site.json', 'C:\\Git\\eqreplay\\Data\\2022_06_28\\Site.json','C:\\Git\\eqreplay\\Data\\2022_06_28\\')