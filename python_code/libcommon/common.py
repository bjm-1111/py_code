#!/sf/vs/bin/python
#-*- coding:utf-8 -*-

#=============================================================================
# Copyright © 2020 bjm
# All rights reserved.
#
# Author: bjm
#
# Last modified: 2020-04-16
#
# Filename: common.py
#
# Description:用于公共函数库
#
#=============================================================================
import time
from subprocess import Popen, PIPE, TimeoutExpired

# 用于函数的参数校检
def param_check(input_type=()):
    """
    对输入参数做检查
    :param input_type:
    :param input: 参数信息（int, str）
    :return: error:except ok:function
    """
    def check_type(elements, type_infos):
        """
        参数校检
        :param elements: 所有参数值
        :param type_infos: 对应类型信息
        :return: True/False
        """
        if len(elements) > len(type_infos):
            raise TypeError("argument count is wrong")
        for value, type_info in zip(elements, type_infos):
            if not isinstance(value, type_info):
                raise TypeError("param({}) type has error".format(value))
        return True

    def _param_check(function):
        def run_fun(*args, **kwargs):
            args_param = list(args)
            kwargs_param = [value for value in kwargs.values()]
            all_param = args_param + kwargs_param
            type_infos = list(input_type)
            check_type(all_param, type_infos)
            return function(*args, **kwargs)
        return run_fun
    return _param_check


# 执行shell命令设置超时
def exec_cmd_limit(cmd, timeout=60):
    """
    执行cmd命令，加上限时
    :param cmd: 命令执行
    :param timeout: 时间(s)
    :return: string/None
    """
    with Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True) as process:
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            if process.returncode != 0:
                raise Exception("exec cmd failed")
            return stdout
        except TimeoutExpired as err:
            process.kill()
            raise Exception("exec cmd timeout:{}".format(err))



@param_check(input_type=(int, int))
def test(value1, value2=0):
    print(value1, value2)


if __name__ == '__main__':
    test(1, value2=2)

