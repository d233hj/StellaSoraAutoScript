"""
作者: d233hj
创建日期: <2023-12-16  15:14:27>
最后编辑时间: <2023-12-16  15:43:27>
最后编辑人员: d233hj
FilePath: \worldTree\tool\tool.py
"""

import os
import subprocess
from pyminitouch import MNTDevice
import cv2
from varname import argname
from PIL import Image
import time
import uiautomator2 as u2
from tool.Config import Config


class AdbTool:
    "模拟器操作工具类"

    __adbConnect = ""
    __image_tmp = ""
    __msg = "None"

    def __init__(self):
        # 读取配置
        configs = Config()
        config_data = configs.loadDb()
        self.__adbConnect = config_data.get("adbConnect")
        self.__image_tmp = config_data.get("img_tmp")
        self.__center = None
        self.__max_val = None

        _DEVICE_ID = self.__adbConnect
        self.device = u2.connect(_DEVICE_ID)

    def __image_to_position_old(self, screen, template):
        "对比图片   \nreturn:__center    图片中心点,\n\t__max_val   相似度"
        # 转为灰度图
        if len(screen.shape) == 3:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        if len(template.shape) == 3:
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        image_x, image_y = template.shape[:2]
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, __max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print("prob:", __max_val)
        if __max_val > 0.75:
            __center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
            self.__center = __center
            self.__max_val = __max_val
        else:
            self.__center = False
            self.__max_val = __max_val

    # 只在调试时使用
    def draw_matches(
        self,
        screen,
        template,
        kp1,
        kp2,
        good_matches,
        mask=None,
        filename="matches.jpg",
    ):
        if mask is not None:
            # 只画内点
            matchesMask = mask.ravel().tolist()
            draw_params = dict(
                matchColor=(0, 255, 0),
                singlePointColor=None,
                matchesMask=matchesMask,
                flags=2,
            )
        else:
            draw_params = dict(matchColor=(0, 255, 0), singlePointColor=None, flags=2)
        img_matches = cv2.drawMatches(
            template, kp1, screen, kp2, good_matches, None, **draw_params
        )
        cv2.imwrite(filename, img_matches)
        #print(f"匹配结果已保存到 {filename}")

    def __image_to_position(self, screen, template):
        """
        使用 SIFT 特征点进行图片匹配（不做离群点过滤）
        """
        # 转为灰度图
        if len(screen.shape) == 3:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        if len(template.shape) == 3:
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # 初始化 SIFT 检测器
        sift = cv2.SIFT_create()

        # 检测关键点和描述符
        kp1, des1 = sift.detectAndCompute(template, None)
        kp2, des2 = sift.detectAndCompute(screen, None)

        if des1 is None or des2 is None or len(kp1) == 0 or len(kp2) == 0:
            print("未检测到足够的特征点")
            self.__center = False
            self.__max_val = 0
            return

        # 创建暴力匹配器并进行KNN匹配
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Lowe's ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        #print(    f"SIFT特征点匹配数量: {len(good_matches)}, 匹配率: {len(good_matches) / max(len(kp1), 1):.2f}")
        self.__max_val = len(good_matches) / max(len(kp1), 1)
        if len(good_matches) > 0 and self.__max_val > 0.2:
            points = [kp2[m.trainIdx].pt for m in good_matches]
            avg_x = sum([p[0] for p in points]) / len(points)
            avg_y = sum([p[1] for p in points]) / len(points)
            self.__center = (avg_x, avg_y)

            # 可视化匹配点
            self.draw_matches(screen, template, kp1, kp2, good_matches)
        else:
            self.__center = False
            self.__max_val

    def capture(self) -> bytes:
        """快速截图，直接截图并作为字节保存在内存中"""
        process = subprocess.Popen(
            "adb -s " + self.__adbConnect + " shell screencap -p",
            shell=True,
            stdout=subprocess.PIPE,
        )
        data = process.stdout.read()
        data = data.replace(b"\r\n", b"\n")
        return data

    def __take_screenshot(self):
        """ "截图"
        os.system("adb shell screencap -p /data/screenshot.png")
        os.system("adb pull /data/screenshot.png " + self.__image_tmp)
        print(self.__image_tmp)"""
        data = self.capture()
        with open(self.__image_tmp, "wb") as f:
            f.write(data)
            f.close()

    def setMsg(self, msg):
        self.__msg = msg

    def getMsg(self):
        return self.__msg

    def adb_click(self, center, offset=(0, 0)):
        (x, y) = center
        x += offset[0]
        y += offset[1]

        self.device.click(x, y)
        # self.device.tap([(x, y)])

        # os.system(f"adb shell input tap {x} {y}")

    def __adb_init(self):
        """os.system("adb connect " + self.__adbConnect)"""
        """_DEVICE_ID = self.__adbConnect
        device = MNTDevice(_DEVICE_ID)"""

    def research_img(self, template, name="img",method="quick"):
        "单纯寻找图片\nreturn:False\n\tTrue"
        self.setMsg("None")
        self.__take_screenshot()
        screen = cv2.imread(self.__image_tmp)
        if method=="quick":
            self.__image_to_position_old(screen, template)
        elif method=="sift":
            self.__image_to_position(screen, template)
        if self.__center != False:
            self.setMsg(
                "#-found img:"
                + str(name)
                + str(self.__center)
                + "\n -"
                + str(self.__max_val)
            )
            return True
        else:
            self.setMsg(
                "#-img not found:"
                + str(name)
                + str(self.__center)
                + "\n -"
                + str(self.__max_val)
            )
            return False

    def apper_to_click(self, template, name="img",method="quick"):
        "匹配图片，如果存在则点击中心\ntemplate:需要查找的图片"
        self.setMsg("None")
        self.__take_screenshot()
        screen = cv2.imread(self.__image_tmp)
        if method=="quick":
            self.__image_to_position_old(screen, template)
        elif method=="sift":    
            self.__image_to_position(screen, template)
        if self.__center != False:
            self.adb_click(self.__center)
            self.setMsg(
                "#~found img:<"
                + str(name)
                + ">, "
                + str(self.__center)
                + "\t "
                + str(self.__max_val)
            )
            print(self.getMsg())
            return True
        else:
            self.setMsg(
                "#-img not found:"
                + str(name)
                + str(self.__center)
                + "\n -"
                + str(self.__max_val)
            )
            return False
