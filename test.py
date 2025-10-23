'''
作者: d233hj
创建日期: <2025-10-23  15:54:10>
最后编辑时间: <2025-10-23  22:46:40>
最后编辑人员: d233hj
FilePath: \StellaSora\test.py
'''

"""from tool.AdbTool import AdbTool
import time

adbTool = AdbTool()

app = adbTool.device.app_list()
print(app)
adbTool.device.app_stop("com.huanmeng.zhanjian2")
time.sleep(3)
adbTool.device.app_start("com.huanmeng.zhanjian2")
"""

"""str1 = "sadas1224"
count = str1.__len__()
print(count)
print(int(str1[str1.__len__() - 1]) + 4)
"""
from tool.AdbTool import AdbTool
from tool.ImgMaster import ImgMaster
img =ImgMaster("./img/nomal")
adbTool = AdbTool()
adbTool.research_img(img.getImg("jiesuan").getImg(),"jiesuan")
print(adbTool.getMsg())