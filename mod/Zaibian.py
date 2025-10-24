from tool.AdbTool import AdbTool
from tool.ImgMaster import ImgMaster
import time
import datetime
from tool.Database import Database
import func_timeout
from tool.Config import Config


class Zaibian:
    def __init__(self):
        configs = Config()
        config_data = configs.loadDb()
        self.imgNomal = ImgMaster()
        self.adbtool = AdbTool()
        self.database = Database()
        self.database.loadDb()
        # 计数
        self.__cardsTime = self.database.data["cardsTime"]
        self.__fightTime = 0
        self.__newcard = self.database.data["newcard"]
        self.__lastcard = self.database.data["lastcard"]
        # 计时
        self._startTime_ = 0

    def zaibianMaster(self, times: int = 1):
        # 计时
        self._startTime__ = time.perf_counter()
        self._startTimeStr__ = datetime.datetime.now()
        allTimes = times
        while times > 0:
            self.__fightTime += 1
            self.timecat(allTimes)
            self.timecount()
            self.zaibian()
            times -= 1
            if self.database.data["newcard"] == self.database.data["gamecards"]:
                print("检测到图鉴卡已经集齐，停止脚本")
                return True

        return True

    def zaibian(self):
        timeout = 10
        # 进入战斗
        while True:

            if timeout <= 0:
                if self.adbtool.research_img(
                    self.imgNomal.getImg("zhandouZ1").getImg(), "zhandouZ1"
                ):
                    self.adbtool.adb_click(center=(700, 700))
                    timeout = 10
                    continue
                print("#1#寻找战斗超时，退出")
                return False
            # 寻找进图按钮
            if self.adbtool.research_img(
                self.imgNomal.getImg("qianwanTZ").getImg(), "qianwanTZ"
            ):
                self.adbtool.apper_to_click(
                    self.imgNomal.getImg("qianwanTZ").getImg(), "qianwanTZ"
                )
                time.sleep(10)
            # 寻找战斗中标志
            if self.adbtool.research_img(
                self.imgNomal.getImg("zhandouZ").getImg(), "zhandouZ"
            ):
                time.sleep(4)
                break
            timeout -= 1

        # 战斗中
        timeout = 10
        while True:

            if timeout <= 0:
                print("#2#战斗等待超时，退出")
                return False
            # 战斗中
            if self.adbtool.research_img(
                self.imgNomal.getImg("zhandouZ").getImg(), "zhandouZ"
            ):
                time.sleep(5)
                continue
            # 选卡逻辑
            elif self.adbtool.research_img(
                self.imgNomal.getImg("xuanka").getImg(), "xuanka", "sift"
            ):
                if self.__xuanka():
                    timeout = 10
                time.sleep(5)
                continue
            # 战斗结束
            if self.adbtool.research_img(
                self.imgNomal.getImg("chonxinZD").getImg(), "chonxinZD"
            ) or self.adbtool.research_img(
                self.imgNomal.getImg("jiesuan").getImg(), "jiesuan"
            ):
                self.adbtool.apper_to_click(
                    self.imgNomal.getImg("quxiao").getImg(), "quxiao"
                )
                while True:
                    if self.adbtool.research_img(
                        self.imgNomal.getImg("jiesuan").getImg(), "jiesuan"
                    ):
                        time.sleep(2)
                        self.adbtool.adb_click(center=(700, 700))
                        continue
                    if self.adbtool.research_img(
                        self.imgNomal.getImg("qianwanTZ").getImg(), "qianwanTZ"
                    ):
                        return True
            timeout -= 1

    # 选卡逻辑
    def __xuanka(self):
        timeout = 9
        self.__cardsTime += 1
        self.__lastcard += 1
        while True:
            # 确认是否存在选卡界面
            if not self.adbtool.research_img(
                self.imgNomal.getImg("xuanka").getImg(), "xuanka", "sift"
            ):
                timeout -= 1
                time.sleep(4)
                if timeout <= 0:
                    print("#3#选卡超时，退出")
                    return False

            # 点击未收录卡牌
            if self.adbtool.apper_to_click(
                self.imgNomal.getImg("weishouL").getImg(), "weishouL"
            ):
                timeout1 = 5
                while True:
                    if timeout1 <= 0:
                        print("#4#选卡超时，退出")
                        return False
                    if self.adbtool.apper_to_click(
                        self.imgNomal.getImg("nazou").getImg(), "nazou"
                    ):
                        break
                    timeout1 -= 1
                self.__newcard += 1
                self.__lastcard = 0
                return True

            # 点击刷新
            if self.adbtool.apper_to_click(
                self.imgNomal.getImg("shuaxin").getImg(), "shuaxin"
            ):
                self.__cardsTime += 1
                time.sleep(1)
                continue

            # 选择已有卡牌
            if self.adbtool.apper_to_click(
                self.imgNomal.getImg("xuanka").getImg(), "xuanka", "sift"
            ):
                timeout1 = 5
                while True:
                    if timeout1 <= 0:
                        print("#4#选卡超时，退出")
                        return False
                    if self.adbtool.apper_to_click(
                        self.imgNomal.getImg("nazou").getImg(), "nazou"
                    ):
                        break
                    timeout1 -= 1

                return True

    def timecat(self, allTimes: int):
        "计算当前时间和开始时间，估计预期结束时间"
        timenow = time.perf_counter()
        costtime = timenow - self._startTime__
        futuretime = (
            float(allTimes - self.__fightTime) / (self.__fightTime)
        ) * costtime

        hours = int(futuretime // 3600)
        minutes = int((futuretime % 3600) // 60)
        print(
            "========# All Times:"
            + str(allTimes)
            + " | The restTimes:"
            + str(self.__fightTime)
            + "|| StartTime: <"
            + str(self._startTimeStr__)
            + ">  PreTime: <"
            + str(hours)
            + "h"
            + str(minutes)
            + "m>  #========"
        )

    def timecount(self):
        "计算卡牌刷新次数，以便自动停止"
        self.database.loadDb()
        self.database.data.update(
            {
                "gamecards": self.database.data["gamecards"],
                "newcard": self.__newcard,
                "cardsTime": self.__cardsTime,
                "lastcard": self.__lastcard,
            }
        )
        self.database.writeDb()
        print(
            "-------<< all Cards: "
            + str(self.database.data["gamecards"])
            + " | New Cards: "
            + str(self.database.data["newcard"])
            + " | Last Card: "
            + str(self.database.data["lastcard"])
            + " >>-------"
        )
