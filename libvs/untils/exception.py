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
# Description: 异常的集合类
#
"""
from error import FileErrorInfo

class ExpBase(Exception):
    """
    异常信息的基类
    """
    def __init__(self, **kwargs):
        self._message = kwargs.pop('message', "")
        self._errno = kwargs.pop('errno', "")
        self._message = self._message.format(**kwargs)
        self._data = {"errno": self._errno, "message": self._message,}
        print(self._data)

class FileNotExist(ExpBase):
    def __init__(self, **kwargs):
        message = kwargs.pop('errmsg', None)
        errno = kwargs.pop('errno', FileErrorInfo.FILE_NOT_EXIST)
        message = message or FileErrorInfo.ERROR_INFO[errno]
        super(FileNotExist, self).__init__(message=message, errno=errno, **kwargs)

class FileTypeError(ExpBase):
    def __init__(self, **kwargs):
        message = kwargs.pop('errmsg', None)
        errno = kwargs.pop('errno', FileErrorInfo.FILE_TYPE_ERROR)
        message = message or FileErrorInfo.ERROR_INFO[errno]
        super(FileTypeError, self).__init__(message=message, errno=errno, **kwargs)

class GetFileSizeFail(ExpBase):
    def __init__(self, **kwargs):
        message = kwargs.pop('errmsg', None)
        errno = kwargs.pop('errno', FileErrorInfo.GET_FILE_SIZE_FAIL)
        message = message or FileErrorInfo.ERROR_INFO[errno]
        super(GetFileSizeFail, self).__init__(message=message, errno=errno, **kwargs)

class ReadFileFail(ExpBase):
    def __init__(self, **kwargs):
        message = kwargs.pop('errmsg', None)
        errno = kwargs.pop('errno', FileErrorInfo.READ_FILE_FAIL)
        message = message or FileErrorInfo.ERROR_INFO[errno]
        super(ReadFileFail, self).__init__(message=message, errno=errno, **kwargs)

class WriteFileFail(ExpBase):
    def __init__(self, **kwargs):
        message = kwargs.pop('errmsg', None)
        errno = kwargs.pop('errno', FileErrorInfo.WRITE_FILE_FAIL)
        message = message or FileErrorInfo.ERROR_INFO[errno]
        super(WriteFileFail, self).__init__(message=message, errno=errno, **kwargs)