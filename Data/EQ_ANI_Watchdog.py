import time
from datetime import datetime
import os
import watchdog
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler
import EQ_ANI_Transform as Transform
import pathlib
import sys
import argparse
import json
import ast
import subprocess

sys.path.insert(0, '.\\Source\\')
from EQ_Animation import Animation

def toTransform(event):
        filename = os.path.basename(event.src_path)
        filepath = os.path.normpath(event.src_path)
        folderpath = pathlib.PurePath(os.path.normpath(event.src_path)).parent
        foldername = os.path.split(folderpath)[-1]
        Event = os.path.basename(folderpath)

        if filename.endswith('_Alarm.json') and not filename.startswith("Trans"):
            #print(f"Filename: {filename}\nFilepath: {filepath}\nFolder: {folderpath}")
            try:
                Transform.dataTransfer.alarmData(filename, filepath, folderpath)

            except Exception as e:
                print(e)
                
        elif filename.endswith('_Site.json') and not filename.startswith("Trans"):
            #print(f"Filename: {filename}\nFilepath: {filepath}\nFolder: {folderpath}")
            try:
                Transform.dataTransfer.siteData(filename, filepath, folderpath)

            except Exception as e:
                print(e)

def collectDataFiles(event):
    try:
        with open(event[3], "r", encoding="utf-8") as f:
            data = ast.literal_eval(f.read())
            eventTime = datetime.strptime(data["EventTime"], "%Y/%m/%d %H:%M:%S.%f")
            filenames = next(os.walk(event[4]), (None, None, []))[2]
            selectFiles = [os.path.join(os.getcwd(), event[4], event[2])]
            for file in filenames:
                print(file)
                if file.startswith("Trans"):
                    FileTime = datetime.strptime(f"{event[5]} {file[6:18]}", "%Y_%m_%d %H_%M_%S.%f")

                    if abs(eventTime.timestamp() - FileTime.timestamp()) <= 30:
                        selectFiles.append(os.path.join(os.getcwd(), event[4], file))
            if len(selectFiles) == 3:
                return selectFiles
            else:
                return []
    except Exception as e:
        pass

class ObsHandler(PatternMatchingEventHandler):
    
    def on_created(self, event):
        if event.is_directory == False:
            filename = os.path.basename(event.src_path)
            filepath = os.path.normpath(event.src_path)
            folderpath = pathlib.PurePath(os.path.normpath(event.src_path)).parent
            #print("""{filename} Created!!!""".format(filename=filename))
            toTransform(event)
                
    def on_deleted(self, event):
        print(event)
        print(f"what the f**k! Someone deleted {event.src_path}!")

    def on_modified(self, event):
        global CWB_FILE, Site_FILE, Alarm_FILE
        #[ trigger, receivedTime, fileName, pathToFile, pathToFolder, foldername ]
        if type(event) == watchdog.events.FileModifiedEvent:
            print(type(event))
            filename = os.path.basename(event.src_path)
            filepath = os.path.normpath(event.src_path)
            folderpath = pathlib.PurePath(os.path.normpath(event.src_path)).parent
            foldername = os.path.split(folderpath)[-1]
            Event = os.path.basename(folderpath)
            # print("""{filename} has been modified!!!""".format(filename=filename))
            
            if filename.endswith('_Alarm.json') and not filename.startswith("Trans"):
                print(f"Filename: {filename}\nFilepath: {filepath}\nFolder: {folderpath}")
                try:
                    Transform.dataTransfer.alarmData(filename, filepath, folderpath)
                    Alarm_FILE = [True, datetime.now(), filename, os.path.join(os.getcwd(), folderpath, filename), os.path.join(os.getcwd(), folderpath), foldername]
                except Exception as e:
                    print(e)
                    
            elif filename.endswith('_Site.json') and not filename.startswith("Trans"):
                print(f"Filename: {filename}\nFilepath: {filepath}\nFolder: {folderpath}")
                try:
                    Transform.dataTransfer.siteData(filename, filepath, folderpath)
                    Site_FILE = [True, datetime.now(), filename, os.path.join(os.getcwd(), folderpath, filename), os.path.join(os.getcwd(), folderpath), foldername]

                except Exception as e:
                    print(e)
                    
            if filename.startswith("CWB") and filename.endswith(".txt"):
                
                print(datetime.now(), 'CWB Event detected.')
                CWB_FILE = [True, datetime.now(), filename, os.path.join(os.getcwd(), folderpath, filename), os.path.join(os.getcwd(), folderpath), foldername]

    # def on_moved(self, event): ##修改檔名最後一步即為將檔案放置於原路徑, 也會用到Moved
    #     filename = os.path.basename(event.dest_path)
    #     filepath = os.path.normpath(event.dest_path)
    #     folderpath = pathlib.PurePath(os.path.normpath(event.dest_path)).parent
    #     print("""{filename} has been moved!!!""".format(filename=filename))
        
    #     if filename.startswith('Alarm'):
    #         print(f"Filename: {filename}\nFilepath: {filepath}\nFolder: {folderpath}")
    #         Transform.dataTransfer.alarmData(filename, filepath, folderpath)
    #     elif filename.startswith('Site'):
    #         pass




if __name__ == '__main__':
    #TODO: 目前已完成CWB_FILE時間寫入, 還須完成Site_FILE時間寫入即Alarm_FILE時間比對, 並用CWB_FILE的時間選取適當的Site_FILE, Alarm_FILE.
    global CWB_FILE, Site_FILE, Alarm_FILE
    
    CWB_FILE = [False]
    Site_FILE = [False]
    Alarm_FILE = [False]
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--folder", help="assign absolute path to activate the watch dog.")
    parser.add_argument('-e', "--env", help="assign environment variables.")
    
    args = parser.parse_args()
    path = args.folder
    env = args.env
    if not os.path.isdir(path):
        print(path, 'is not a directory.')
        sys.exit()
    pattern = ["*"]
    ignore_patterns = None
    ignore_directories = None
    case_sensitive = True
    # event_handler = PatternMatchingEventHandler(pattern, ignore_patterns, ignore_directories, case_sensitive)
    
    # event_handler.on_created = on_created
    # event_handler.on_deleted = on_deleted
    # event_handler.on_modified = on_modified
    # event_handler.on_moved = on_moved
    event_handler = ObsHandler()
    go_recusively = True
    my_observer = Observer()
    my_observer.schedule(event_handler, path, recursive=go_recusively)
    my_observer.start()
    print(f'WatchDog is on...\nWatching {path}')
    
    try:
        while 1:
            time.sleep(1)
            if CWB_FILE[0]:
                print(CWB_FILE)
                print(120 - abs(datetime.now().timestamp() - CWB_FILE[1].timestamp()), "seconds left.")
                if abs(datetime.now().timestamp() - CWB_FILE[1].timestamp()) >= 10:
                    
                    print('time has arrived, choose files to create gif.')
                    files = collectDataFiles(CWB_FILE)
                    print('selectFiles:', files)
                    Ani = Animation(dataFiles=files)
                    Ani.draw()
                    gifPath = Ani.creategif()
                    print(gifPath)
                    CWB_FILE = [False]
                    Site_FILE = [False]
                    Alarm_FILE = [False]
                
    except KeyboardInterrupt:
        my_observer.stop()
    my_observer.join()