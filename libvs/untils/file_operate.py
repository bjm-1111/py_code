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
import logger

log = logger.LogHandler(__name__, stream=False)


class BaseFile(object):
    """
    Basic operation base class of file
    """
    def __init__(self, file_path):
        self._file_path = file_path
        #是否存在的标记
        self._is_exist = None

    @property
    def file_path(self):
        return self._file_path

    @property
    def is_exist(self):
        self._is_exist = os.path.exists(self._file_path)
        return self._is_exist

    def read_lines_to_list(self):
        """
        按照行读取（数据过大读取会有问题）
        :return: 一个列表
        """
        if not self.is_exist:
            raise IOError("file path not exist:({})".format(self.file_path))
        with open(self.file_path, "r", encoding="utf-8") as f_read:
            return f_read.readlines()

    def read_lines_to_iterator(self):
        """
        按行读取，返回迭代器
        :return: 返回一个迭代器
        """
        if not self.is_exist:
            raise IOError("file path not exist:({})".format(self.file_path))
        with open(self.file_path, "r", encoding="utf-8") as f_read:
            for line in f_read:
                yield line

    def _append_linefeed(self, file_info):
        """
        给文本信息添加换行符
        :param file_info:
        :return:
        """
        file_info_list = [info + "\n" for info in file_info]
        return file_info_list

    def write_lines_to_file(self, file_info, mode="a"):
        """
        通过行的方式写
        :param file_info:需要写入的文件信息(列表)
        :return: True/False/或者抛出异常
        """
        if not file_info or not isinstance(file_info, list):
            return False
        try:
            file_info_list = self._append_linefeed(file_info)
            with open(self.file_path, mode, encoding="utf-8") as f_write:
                f_write.writelines(file_info_list)
            return True
        except Exception as exp:
            raise IOError("write failed:{}".format(exp))

class JsonFile(BaseFile):

    def __init__(self, file_path):
        super(JsonFile, self).__init__(file_path)

    def load_file(self, mode="json"):
        if not self.is_exist:
            raise IOError("file path not exist:({})".format(self.file_path))
        mode_list = ["JSON", "J", "DICT", "D"]
        with open(self.file_path, "r", encoding="utf-8") as f_read:
            file_info = json.load(f_read)
            if mode.upper() not in mode_list:
                return json.dumps(file_info)
        return file_info

    def dump_file(self, file_info, mode="dict"):
        """
        写文件
        :param file_info: 写入的信息
        :param mode: 是字符串还是json类型的数据
        :return: True/False/异常
        """
        mode_list = ["JSON", "J", "DICT", "D", "LIST", "L"]
        if mode not in mode_list:
            file_info = json.loads(file_info)
        if not file_info or (not isinstance(file_info, dict) and not isinstance(file_info, list)):
            return False
        try:
            with open(self.file_path, "w", encoding="utf-8") as f_write:
                json.dump(file_info, f_write, ensure_ascii=False, indent=4)
            return True
        except Exception as exp:
            raise IOError("write failed:{}".format(exp))

if __name__ == "__main__":

    try:
        file_path = ["D:\\my_code\\python_code\\py_code\\libvs\\untils\\test.json", "\nsss"]
        file_path_txt = "D:\\my_code\\python_code\\py_code\\libvs\\untils\\记录.txt"
        file_path_json = "D:\\my_code\\python_code\\py_code\\libvs\\untils\\test.json"
        file = JsonFile(file_path_json)
        count = 0
        print(file.dump_file('[{"name": "bjm", "age": "2222", "email": "xxxx@163.com"}]', mode="string"))
    except Exception as exp:
        print(exp)




