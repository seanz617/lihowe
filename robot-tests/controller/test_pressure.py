# -*- coding: utf-8 -*-

from multiprocessing import Pool, cpu_count
from functools import wraps
from robot.api import logger

from base import base
from test_poss import test_poss


def pressure(func):
    """ Pressure test wrapper
    Args:
        func: wrapped function name
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        dict_param = base.parse_param(args[1])
        try:
            processes_num = int(dict_param.get("processes", 2 * cpu_count()))
            concurrent_num = int(dict_param.get("concurrent", 10))
        except ValueError:
            concurrent_num = 10
            processes_num = 2 * cpu_count()
            logger.info("Parameter convert failed, default: concurrent num is 10, processes num is 2 * cpu_count",
                        html=True,
                        also_console=True)

        result_list = list()
        with Pool(processes=processes_num) as pool:
            for i in range(concurrent_num):
                result_list.append(pool.apply_async(func(*args, **kwargs)))
            pool.close()
            pool.join()

    return wrapper


class TestPressure(base):
    """ Pressure test """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        """ init """
        base.__init__(self, self.__class__.__name__)

    @staticmethod
    def pressure_test(func):
        """ Pressure test wrapper
        Args:
            func: wrapped function name
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            dict_param = base.parse_param(args[1])
            try:
                processes_num = int(dict_param.get("processes", 2 * cpu_count()))
                concurrent_num = int(dict_param.get("concurrent", 10))
            except ValueError:
                concurrent_num = 10
                processes_num = 2 * cpu_count()
                logger.info("Parameter convert failed, default: concurrent num is 10, processes num is 2 * cpu_count",
                            html=True,
                            also_console=True)

            result_list = list()
            with Pool(processes=processes_num) as pool:
                for i in range(concurrent_num):
                    result_list.append(pool.apply_async(func(*args, **kwargs)))
                pool.close()
                pool.join()

        return wrapper

    @pressure
    def put_object_pressure(self, dict_param):
        """  """
        test_poss().put_object(dict_param)

    @pressure
    def get_object_pressure(self, dict_param, share_code=""):
        """  """
        test_poss().get_object(dict_param, share_code)


if "__main__" == __name__:
    TestPressure().put_object_pressure({"key": "", "body": "32M", "copies": 2})
