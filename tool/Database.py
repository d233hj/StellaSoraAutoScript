'''
作者: d233hj
创建日期: <2025-10-23  15:54:10>
最后编辑时间: <2025-10-23  16:02:00>
最后编辑人员: d233hj
FilePath: \StellaSora\tool\Database.py
'''

import json


class Database:
    "存储脚本运行信息"

    _dataSrc = "./data/"
    _jsonName = "data.json"

    def __init__(self, jsonName="") -> None:
        self._jsonName = jsonName if jsonName != "" else self._jsonName

    def writeDb(self):
        with open(self._dataSrc + self._jsonName, "w") as json_file:
            json.dump(self.data, json_file, indent=4)

    def loadDb(self):
        with open(self._dataSrc + self._jsonName, "r") as json_file:
            self.data = json.load(json_file)
        return self.data
