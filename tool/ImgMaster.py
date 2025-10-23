"""
作者: d233hj
创建日期: <2025-10-23  15:54:10>
最后编辑时间: <2025-10-23  16:44:27>
最后编辑人员: d233hj
FilePath: \StellaSora\tool\ImgMaster.py
"""

import os
from queue import Full
import cv2
from PIL import Image
from tool.Img import Img
from tool.Config import Config


class ImgMaster:
    "图片管理与导入，用于脚本将用到的大量ui图片"

    _srcImg = ""
    _imgDict = {}

    def __init__(self, srcImg: str = None):
        configs = Config()
        config_data = configs.loadDb()
        "遍历图像目录，创建单个图片对象并装入字典"
        if srcImg != None:
            self._srcImg = srcImg
        else:
            self._srcImg = config_data.get("img_nomal")
        paths = os.walk(self._srcImg)
        for path, dir_lst, file_lst in paths:
            for file_name in file_lst:
                imgSrc = os.path.join(path, file_name)
                img = Img(file_name, imgSrc)
                self._imgDict.update({file_name: img})

    def getImg(self, imgName: str) -> Img:
        imgName = imgName + ".png"
        return self._imgDict[imgName]
