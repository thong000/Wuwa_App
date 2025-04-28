import json,os,time,threading
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from const import ROOT_DIR
import logging
import os
from datetime import datetime,timedelta


today = datetime.now().strftime("%Y-%m-%d")
formatter = logging.Formatter('%(asctime)s - %(message)s')



def debugLog(message):
    debug_logger = logging.getLogger('debug')
    debug_logger.setLevel(logging.DEBUG)
    debug_handler = logging.FileHandler(f"{ROOT_DIR}/log/{today}_debug.log", encoding='utf-8')  # ✅ UTF-8
    debug_handler.setFormatter(formatter)
    debug_logger.addHandler(debug_handler)
    #debug_logger.debug(message)
def errorLog(message):
    error_logger = logging.getLogger('error')
    error_logger.setLevel(logging.ERROR)
    error_handler = logging.FileHandler(f"{ROOT_DIR}/log/{today}_error.log", encoding='utf-8') # ✅ UTF-8
    error_handler.setFormatter(formatter)
    error_logger.addHandler(error_handler)
    #error_logger.error(message)
def appLog(message):
    app_logger = logging.getLogger('app')
    app_logger.setLevel(logging.INFO)
    app_handler = logging.FileHandler(f"{ROOT_DIR}/log/{today}_app__.log", encoding='utf-8')  # ✅ UTF-8
    app_handler.setFormatter(formatter)
    app_logger.addHandler(app_handler)
    #app_logger.info(message)
    
def deleteOldLogs(log_dir='.', days=5):
    now = datetime.now()
    for filename in os.listdir(log_dir):
        if filename.endswith(".log") and filename[:10].count('-') == 2:
            try:
                file_date = datetime.strptime(filename[:10], "%Y-%m-%d")
                if now - file_date > timedelta(days=days):
                    file_path = os.path.join(log_dir, filename)
                    os.remove(file_path)
            except ValueError:
                pass



def readJson(filePath,rootDir):
    """ Read a json file

    Args:
        filePath (str): a path of file.
        rootDir: a path to main.py file

    Returns:
        None: if cant read the file
        str: content of the json file
        
    """
    filePath=rootDir+"/"+filePath
    if not os.path.isfile(filePath):
        debugLog(f"readJson(core/fileHandler):\n {filePath} not found")
        return None
    with open(filePath, 'r', encoding='utf-8') as file:
        return json.load(file)

        
def printDictPretty(dict):
    """ Print dictionary with pretty format

    Args:
        dict (dict): a dict need to print in pretty format
    """
    print(json.dumps(dict, indent=4, ensure_ascii=False))
    
    
class FileTracking(FileSystemEventHandler):
    """ Tracking a file, if it is on modified perform some function
    
    """
    def __init__(self, filePath, callback, delay=0.2):
        super().__init__()
        self.filePath = os.path.abspath(filePath)
        self.callback = callback
        self.delay = delay
        self._timer = None

    def on_modified(self, event):
        debugLog(f"on_modified (core/fileHandler):\nFile {self.filePath} is on modified")
        if os.path.abspath(event.src_path) == self.filePath:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self.delay, self.callback)
            self._timer.start()


def readTextFileToList(filePath: str) -> list[str]:
    """ Read txt file to make a list

    Args:
        filePath (str): a path to a txt file

    Returns:
        list[str]: each line in file is a value of the list
    """
    with open(ROOT_DIR+"/"+filePath, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines






def appendJson(key, new_dict, filename,root):
    """ Add a dict to json file as one element 
    
    Parameters:
        key (str): Khóa để lưu dictionary mới
        new_dict (dict): Dictionary need to add
        filename (str): file name
        root (str): a path to main file
    """
    filename=root+"/"+filename
    filepath = Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    if os.path.exists(filename):

        with open(filename, 'r', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}
    
    existing_data[key] = new_dict
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)



        
def deleteKeyFromJson(filePath, keyToDelete,root):
    filePath=root+"/"+filePath
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if keyToDelete in data:
            del data[keyToDelete]
            with open(filePath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Đã xóa key '{keyToDelete}' khỏi file.")
        else:
            print(f"Không tìm thấy key '{keyToDelete}' trong file.")
    except Exception as e:
        print(f"Lỗi: {e}")


def removeKeyByShift(filename, keyToRemove,root):

    filename=root+"/"+filename
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if keyToRemove not in data:
        print(f"Key '{keyToRemove}' không tồn tại.")
        return


    keys = list(data.keys())
    values = list(data.values())


    index = keys.index(keyToRemove)


    for i in range(index, len(keys) - 1):
        values[i] = values[i+1]


    keys.pop()
    values.pop()


    newData = dict(zip(keys, values))


    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(newData, f, indent=4, ensure_ascii=False)

    print(f"Đã xoá key '{keyToRemove}' thành công.")