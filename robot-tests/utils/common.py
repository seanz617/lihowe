import os
import time
import random
import psutil
import hashlib
from robot.api import logger


def check_file_exists(file_name):
    assert os.path.exists(file_name)


def gen_name(label):
    return "{}-{}".format(label, "".join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRETUVWXYZ", 16)))


def get_timestamp():
    return int(time.time())


def read_chunks(obj, size):
    """  """
    obj.seek(0)
    chunk = obj.read(size)
    while chunk:
        # chunk = chunk.encode("utf-8")
        yield chunk
        chunk = obj.read(size)
    else:
        obj.seek(0)


def calc_file_md5(file_path):
    """ Calculation file hash use md5 """
    hash_md5 = str()
    method = hashlib.md5()
    if not os.path.exists(file_path):
        logger.error("File(%s) don not exist, can not calculation file hash" % file_path)
        return hash_md5

    with open(file_path, 'rb') as f:
        for chunk in read_chunks(f, 1024 * 1024):
            method.update(chunk)
    return method.hexdigest()


def get_process_info(name):
    """ Fetch the process info """
    process_lst = list()
    all_pid = psutil.pids()
    for pid in all_pid:
        info = psutil.Process(pid)
        if name in info.name():
            process_lst.append(info)

    return process_lst


def get_cpu_memory_info(process_name):
    """ Fetch the process of cpu and memory info """
    info_dict = dict()
    try:
        process_list = get_process_info(process_name)
        for process in process_list:
            cmdline = process.cmdline()
            name = os.path.basename(cmdline[2]) if len(cmdline) > 3 else process_name + "_" + str(process.pid)
            name = process_name + "_" + str(process.pid) if not name else name
            cpu_info = process.cpu_percent(3)
            memory_info = process.memory_full_info()
            info_dict.update({name: {"cpu": cpu_info, "memory": memory_info}})
    except Exception as e:
        logger.error("Fetch the process %s of cpu and memory info err: %s" % (process_name, e), html=True)

    return info_dict


if __name__ == "__main__":
    # path = r"D:\download\adfad.mkv"
    # file_hash = calc_file_md5(path)
    # print(file_hash)
    info_dict = get_cpu_memory_info("pcdn")
    print(info_dict)
