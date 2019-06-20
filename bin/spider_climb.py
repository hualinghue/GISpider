import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import GetImgAddress,customize_class
import inspect
if __name__ == "__main__":
    for name, obj in inspect.getmembers(customize_class):  #遍历所有自定义采集信息对象
        if inspect.isclass(obj) and name!='Options' and obj.display:     #筛选符合的对象
            bb = GetImgAddress.DriveEngine(obj())
            bb.run()