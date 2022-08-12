import time
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import Transform
import pathlib
import sys
from IPython import get_ipython
sys.path.insert(0, '..\\Source\\')
from EQ_Animation_functionalized import Animation


def on_created(event):
    if event.is_directory == False:
        filename = os.path.basename(event.src_path)
        filepath = os.path.normpath(event.src_path)
        folderpath = pathlib.PurePath(os.path.normpath(event.src_path)).parent
        print("""{filename} Created!!!""".format(filename=filename))
        
        if filename == ('Finish'):
            print('Finish')
            
def on_deleted(event):
    print(event)
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    if event.is_directory == False:
        filename = os.path.basename(event.src_path)
        filepath = os.path.normpath(event.src_path)
        folderpath = pathlib.PurePath(os.path.normpath(event.src_path)).parent
        Event = os.path.basename(folderpath)
        print("""{filename} has been modified!!!""".format(filename=filename))
        
        if filename.startswith('Alarm'):
            print(f"Filename: {filename}\nFilepath: {filepath}\nFolder: {folderpath}")
            try:
                Transform.dataTransfer.alarmData(filename, filepath, folderpath)
                #draw = Animation('2022_03_23', 1, 80)
                #draw.draw()
            except Exception as e:
                print(e)
                
        elif filename.startswith('Site'):
            print(f"Filename: {filename}\nFilepath: {filepath}\nFolder: {folderpath}")
            try:
                Transform.dataTransfer.siteData(filename, filepath, folderpath)
                #draw = Animation('2022_03_23', 1, 80)
                #draw.draw()
            except Exception as e:
                print(e)

# def on_moved(event): ##修改檔名最後一步即為將檔案放置於原路徑, 也會用到Moved
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
    
    pattern = ["*"]
    ignore_patterns = None
    ignore_directories = None
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(pattern, ignore_patterns, ignore_directories, case_sensitive)
    
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    # event_handler.on_moved = on_moved
    
    path = os.getcwd()
    go_recusively = True
    my_observer = Observer()
    my_observer.schedule(event_handler, path, recursive=go_recusively)
    my_observer.start()
    print('WatchDog is on...')
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
    my_observer.join()