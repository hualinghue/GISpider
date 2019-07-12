import os,sys
from multiprocessing import Pool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import GetImgAddress,customize_class
import inspect
if __name__ == "__main__":
    pool = Pool(8)
    for name, obj in inspect.getmembers(customize_class):  #遍历所有自定义采集信息对象
        if inspect.isclass(obj) and name!='Options' and obj.display:     #筛选符合的对象
            print(1)
            bb = GetImgAddress.DriveEngine(obj())
            pool.apply_async(bb.run())
    print('---staty---')
    pool.close()  # 关闭线程池，关闭后不再接受进的请求
    pool.join()#等待进程池所有进程都执行完毕后，开始执行下面语句
    print("--end--")