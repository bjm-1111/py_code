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


class FileBaseInfo(object):
    """
    文件操作的基础类
    """
    def __init__(self, file_path, file_type=None):

        self._file_path = file_path
        self._file_type = file_type
        log.info("文件路径为：{}".format(self._file_path))
        log.info("文件类型为：{}".format(self._file_type))

        if not self.is_exist():
            log.error("文件路径不存在：{}".format(self._file_path))
            raise exception.FileNotExist(file_path=self.file_path, exp="")

        if not self.is_type_curr():
            log.error("当前只支持此文件类型：{}".format(self._file_type))
            raise exception.FileTypeError(file_type=self.file_type, exp="")

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
            log.info("文件路径为：{}".format(file_path))
            if file_path == None:
                file_path =self.file_path
            kb_unit = 1024
            mb_unit = kb_unit * 1024
            gb_unit = mb_unit * 1024
            tb_unit = gb_unit * 1024

            file_size = os.path.getsize(file_path)
            log.info("文件大小：{}字节".format(file_size))
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
            log.error("获取文件大小失败,err：{}".format(str(exp)))
            raise exception.GetFileSizeFail(file_path=file_path, exp=str(exp))

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
            with open(self.file_path, "r", encoding="utf-8") as f_read:
                file_info = json.load(f_read)
                file_info = json.dumps(file_info, indent=4,ensure_ascii=False)
            return file_info
        except Exception as exp:
            log.error("读取文件失败：{}".format(str(exp)))
            raise exception.ReadFileFail(file_path=self.file_path, exp=str(exp))

    def read_file(self):
        """
        读取json文件
        :return: 字典（列表）或者抛出异常
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f_read:
                file_info = json.load(f_read)
            return file_info
        except Exception as exp:
            log.error("读取文件失败：{}".format(str(exp)))
            raise exception.ReadFileFail(file_path=self.file_path, exp=str(exp))

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

            with open(self.file_path, "w", encoding="utf-8") as f_write:
                json.dump(file_info, f_write)
            return True
        except Exception as exp:
            log.error("写入文件失败：{}".format(str(exp)))
            raise exception.WriteFileFail(file_path=self.file_path, exp=str(exp))

class TextFileOpe(FileBaseInfo):
    """
    文本文件的操作类
    """
    def __init__(self, file_path):
        file_type = [".txt", ".log"]
        super(TextFileOpe, self).__init__(file_path, file_type=file_type)

    def read_file_line(self):
        """
        按照一行读取文件,用于大文件处理
        :return: 返回一个迭代器/抛出异常
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f_read:
                for line in f_read:
                    yield line
        except Exception as exp:
            log.error("读取文件失败：{}".format(str(exp)))
            raise exception.ReadFileFail(file_path=self.file_path, exp=str(exp))

    def read_file(self):
        """
        全读
        :return: 返回一个列表/抛出异常
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f_read:
                file_info = f_read.readlines()
            return file_info
        except Exception as exp:
            log.error("读取文件失败：{}".format(str(exp)))
            raise exception.ReadFileFail(file_path=self.file_path, exp=str(exp))

    def write_file_line(self, line, mode="a"):
        """
        单行写入(追加)
        :param line:字符串
        :return: True/异常
        """
        try:
            with open(self.file_path, mode, encoding="utf-8") as f_write:
                f_write.write(line)
            return True
        except Exception as exp:
            log.error("写入文件失败：{}".format(str(exp)))
            raise exception.WriteFileFail(file_path=self.file_path, exp=str(exp))

    def write_file_lines(self, lines, mode="a"):
        """
        多行写入(追加)
        :param line:字符串
        :return: True/异常
        """
        try:
            with open(self.file_path, mode, encoding="utf-8") as f_write:
                f_write.writelines(lines)
            return True
        except Exception as exp:
            log.error("写入文件失败：{}".format(str(exp)))
            raise exception.WriteFileFail(file_path=self.file_path, exp=str(exp))





if __name__ == "__main__":
    try:
        file_path = ["D:\\my_code\\python_code\\py_code\\libvs\\untils\\test.json", "\nsss"]
        file_path_txt = "D:\\my_code\\python_code\\py_code\\libvs\\untils\\记录.txt"
        file = TextFileOpe(file_path_txt)
        print(file.write_file_line(file_path))
    except Exception as exp:
        print(exp, "sss")



