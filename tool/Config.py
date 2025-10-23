'''
作者: d233hj
创建日期: <2025-10-23  16:05:45>
最后编辑时间: <2025-10-23  16:21:37>
最后编辑人员: d233hj
FilePath: \StellaSora\tool\config.py
'''
'''
作者: d233hj
创建日期: <2025-10-23  16:05:45>
最后编辑时间: <2025-10-23  16:06:52>
最后编辑人员: d233hj
FilePath: \StellaSora\tool\config.py
'''
import json


class Config:
    "存储脚本配置"

    _dataSrc = "./data/"
    _jsonName = "config.json"

    def __init__(self) -> None:
        self._jsonName = self._jsonName

    def writeDb(self):
        with open(self._dataSrc + self._jsonName, "w") as json_file:
            json.dump(self.data, json_file, indent=4)

    def loadDb(self):
        with open(self._dataSrc + self._jsonName, "r") as json_file:
            self.data = json.load(json_file)
        return self.data
