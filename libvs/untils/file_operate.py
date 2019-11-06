#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
# Copyright
#
# Author: bjm
#
# Last modified:2019 10 6
#
# Filename: file_operate.py
#
# Description: 文件操作集成类
#
"""
import exception
import os
import json


class FileBaseInfo(object):
    """
    文件操作的基础类
    """
    def __init__(self, file_path, file_type=None):

        self._file_path = file_path
        self._file_type = file_type

        if not self.is_exist():
            raise exception.FileNotExist(file_path=self.file_path)

        if not self.is_type_curr():
            raise exception.FileTypeError(file_type=self.file_type)

    @property
    def file_path(self):
        return self._file_path

    @property
    def file_type(self):
        return self._file_type

    def is_exist(self, file_path=None):
        """
        判断文件是否存在
        :param file_path:文件名
        :return: True/False
        """
        if file_path == None:
            file_path = self.file_path
        return os.path.exists(file_path)

    def is_type_curr(self, file_path=None, file_type=None):
        """
        判断文件类型是否正确
        :param file_type: 文件类型
        :return: True/False
        """
        if file_path == None:
            file_path = self.file_path
        if file_type == None:
            file_type = self.file_type
        _, file_type_real = os.path.splitext(file_path)
        if file_type_real not in file_type:
            return False
        return True

    def get_file_size(self, file_path=None, unit="GB"):
        """
        获取文件大小
        :param file_path: 文件路径
        :param unit: 单位
        :return: 文件大小/抛出异常
        """
        try:
            if file_path == None:
                file_path =self.file_path
            kb_unit = 1024
            mb_unit = kb_unit * 1024
            gb_unit = mb_unit * 1024
            tb_unit = gb_unit * 1024

            file_size = os.path.getsize(file_path)
            if unit.upper() == "KB":
                file_size = file_size / kb_unit
            elif unit.upper() == "MB":
                file_size = file_size / mb_unit
            elif unit.upper() == "GB":
                file_size = file_size / gb_unit
            elif unit.upper() == "TB":
                file_size = file_size / tb_unit
            return file_size
        except Exception as exp:
            raise exception.GetFileSizeFail(file_path=file_path)

class JsonFileOpe(FileBaseInfo):
    """
    json类型文件操作
    """
    def __init__(self, file_path):
        file_type = [".json"]
        super(JsonFileOpe, self).__init__(file_path, file_type=file_type)

    def read_file_tostring(self):
        """
        读取json文件,返回字符串信息
        :return: 字符串或者抛出异常
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f_read:
                file_info = json.load(f_read)
                file_info = json.dumps(file_info, indent=4,ensure_ascii=False)
            return file_info
        except Exception as exp:
            raise exception.ReadFileFail(file_path=self.file_path)

    def read_file(self):
        """
        读取json文件
        :return: 字典（列表）或者抛出异常
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f_read:
                file_info = json.load(f_read)
            return file_info
        except Exception as exp:
            raise exception.ReadFileFail(file_path=self.file_path)

    def _set_marks(self, file_info):
        """
        把字符串中的单引号变成双引号
        :param file_info: 文件信息
        :return: 处理完后的字符串
        """
        return file_info.replace("'", "\"")

    def write_file(self, file_info):
        """
        写文件
        :param file_info:
        :return: True/异常
        """
        try:
            if type(file_info) not in (dict, list):
                file_info = json.loads(self._set_marks(file_info))

            with open(file_path, "w", encoding="utf-8") as f_write:
                json.dump(file_info, f_write)
            return True
        except Exception as exp:
            print(exp)
            raise exception.WriteFileFail(file_path=self.file_path)


class TextFileOperate(FileBaseInfo):
    """
    文本文件的操作类
    """
    def __init__(self, file_path):
        file_type = [".txt", ".log"]
        super(JsonFileOpe, self).__init__(file_path, file_type=file_type)





if __name__ == "__main__":

    try:
        file_path = "D:\\my_code\\python_code\\py_code\\libvs\\untils\\test.json"
        file = JsonFileOpe(file_path)
        file_info = "{'name': 'leon', 'age': '30', 'email': 'xxxx@163.com'}"
        print(file.write_file(file_info))
    except Exception as exp:
        print(exp, "sss")
    


