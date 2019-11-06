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
# Description: 错误信息集合类
#
"""

from enum import Enum


class FileErrorInfo(object):
    #错误码集合
    SUCCESS = 0
    BASE = 0xA0270000
    FILE_NOT_EXIST = BASE | 1  # 0xa0270001L
    FILE_TYPE_ERROR = BASE | 2  # 0xa0270002L
    GET_FILE_SIZE_FAIL = BASE | 3  # 0xa0270003L
    READ_FILE_FAIL = BASE | 4  # 0xa0270004L
    WRITE_FILE_FAIL = BASE | 5  # 0xa0270004L
    #错误信息集合
    ERROR_INFO = {
        FILE_NOT_EXIST: u"文件（{file_path}）不存在！错误原因:{exp}。",
        FILE_TYPE_ERROR: u"文件类型（只支持“{file_type}”）不支持！错误原因:{exp}。",
        GET_FILE_SIZE_FAIL: u"获取文件（{file_path}）大小失败！错误原因:{exp}。",
        READ_FILE_FAIL: u"读取文件（{file_path}）内容失败！错误原因:{exp}。",
        WRITE_FILE_FAIL: u"写入文件（{file_path}）失败！错误原因:{exp}。",
    }