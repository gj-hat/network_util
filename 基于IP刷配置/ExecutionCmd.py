"""
 @author：     JiaGuo
 @emil：       1520047927@qq.com
 @date：       Created in 2024/9/12 10:58
 @description：
 @modified By：
 @version:     1.0
"""
import sys
import time
import os
import shutil
import logging.handlers
from concurrent.futures import ThreadPoolExecutor

from Public_Util.PropertiesReader import PropertiesReader
from Public_Util.banner_util import Banner
from Public_Util.file_util import read_file
from Public_Util.netmikoUtil import connect_and_execute


PATTERN = ""
ABSOLUTELYPATH = ''
# 获取当前项目的绝对路径
if getattr(sys, 'frozen', False):
    ABSOLUTELYPATH = os.path.dirname(sys.executable)
else:
    ABSOLUTELYPATH = os.path.dirname(os.path.abspath(__file__))
OUT_PUT_PATH = os.path.join(ABSOLUTELYPATH, 'output')
if os.path.exists(OUT_PUT_PATH):
    shutil.rmtree(OUT_PUT_PATH)
os.mkdir(OUT_PUT_PATH)
CMDLIST_PATH = os.path.join(ABSOLUTELYPATH, 'cmdList.txt')
IPLIST_PATH = os.path.join(ABSOLUTELYPATH, 'ipList.txt')
PARAM_PATH = os.path.join(ABSOLUTELYPATH, 'config.properties')
FILE_LOG_PATH = os.path.join(OUT_PUT_PATH, "控制台输出.log")

"""
日志写入文件  
1. 创建一个日志记录器  （保证唯一，但无卵用 主要得靠下面的配置）
2. 设置日志记录器的日志级别
3. 创建一个标准输出流控制器（可以通过参数选择输出流的位置，默认是标准输出流即控制台）
4. 设置输出流日志格式
5. 将输出流控制器添加到日志控制器中
6. 创建一个文件写入流控制器
    以时间为单位切割日志文件
    filelog = logging.handlers.TimedRotatingFileHandler(os.path.join(path, "控制台输出.log"), when='D', interval=1,backupCount=3)
    以文件大小为单位切割日志文件
    filelog = logging.handlers.RotatingFileHandler(os.path.join(path, "控制台输出.log"), maxBytes=1024 * 1024 * 100,
7. 设置写入日志格式  （也可以设置级别等等）
8. 将文件写入流控制器添加到日志控制器中
"""
logger = logging.getLogger('M1版本-ExecutionCmd')
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console)
filelog = logging.handlers.RotatingFileHandler(FILE_LOG_PATH, maxBytes=10 * 1024 * 1024, backupCount=5)
filelog.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
filelog.setLevel(logging.INFO)
logger.addHandler(filelog)

if __name__ == '__main__':
    logger.debug("\n" +
                 Banner(width=80, border_char='#').create(
                     ["基于ip批量刷配置", "2025年04月09日16:11:47"]))
    time.sleep(3)
    t1 = time.time()
    cmdList = read_file(CMDLIST_PATH)
    ipList = read_file(IPLIST_PATH)
    param = PropertiesReader().read_properties(PARAM_PATH)
    enable_privilege_mode = param.get("identity")
    is_save = param.get("is_save")
    if is_save == "True":
        is_save = True
    else:
        is_save = False
    enable_password = param.get("enable_password")
    global_delay_factor = int(param.get("global_delay_factor", 1))
    retry = int(param.get("retry", 3))
    timeout = int(param.get("timeout", 60))
    conn_timeout = int(param.get("conn_timeout", 10))
    max_workers = int(param.get("max_workers", 50))

    logger.info("----------------------开始处理----------------------")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for ip in ipList:
            future = executor.submit(connect_and_execute,
                                     cmdList,
                                     param.get("device_type"),
                                     ip,
                                     param.get("username"),
                                     param.get("password"),
                                     retry,
                                     enable_privilege_mode,
                                     enable_password,
                                     global_delay_factor,
                                     is_save,
                                     conn_timeout,
                                     timeout,
                                     session_log_path=OUT_PUT_PATH,
                                     reserved_keyword = None
                                     )
            futures.append(future)
        for future in futures:
            re = future.result()
            logger.info(f"处理结果{re}")

    logger.info("-----------处理结束时长:" + str(time.time() - t1) + "----------------")
    print("执行完成，请按任意键退出...")
    input()  # 等待用户输入字符，按任意键退出
