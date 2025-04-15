"""
 @author：     JiaGuo
 @emil：       1520047927@qq.com
 @date：       Created in 2023/11/17 09:41
 @description：
 @modified By：
 @version:     1.0
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import os
import shutil
import logging.handlers
from Public_Util.banner_util import Banner
from Public_Util.excel_util import ExcelUtil
from Public_Util.netmikoUtil import connect_and_execute
from Public_Util.PropertiesReader import PropertiesReader

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
PARAM_PATH = os.path.join(ABSOLUTELYPATH, 'config.properties')
DATA_PATH = os.path.join(ABSOLUTELYPATH, 'data.xlsx')
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

# 读取excel文件
data_excel = ExcelUtil(DATA_PATH)


# 这是增强方法 如果需要对返回结果进行处理 可以在这里进行处理 否则可以直接返回结果
def enhancement_method(in_var):
    data_excel.write_excel_cell(sheet_name="Sheet1", row=in_var.get("reserved_keyword") + 2, column_name="res1",
                                value=in_var.get("data"))
    return in_var


if __name__ == '__main__':
    # aa = {"row_id":2,"data":"<123>sss<s>"}
    # enhancement_method(aa)

    logger.debug("\n" +
                 Banner(width=80, border_char='#').create(
                     ["基于表格批量刷配置", "2025年04月09日16:11:47"]))
    time.sleep(3)
    t1 = time.time()
    param = PropertiesReader().read_properties(PARAM_PATH)
    # netmiko 连接参数
    global_delay_factor = int(param.get("global_delay_factor", 1))
    retry = int(param.get("retry", 3))
    timeout = int(param.get("timeout", 60))
    conn_timeout = int(param.get("conn_timeout", 10))
    max_workers = int(param.get("max_workers", 50))
    # 元数据
    device_type = param.get("device_type")
    username = param.get("username")
    password = param.get("password")
    port = param.get("port")
    identity = param.get("identity")
    is_save = param.get("is_save")
    enable_password = param.get("enable_password")

    # 拿到需要执行命令的设备信息
    input_command_data = (data_excel.read_excel_dict(sheet_name="Sheet1"))
    # 拿到设备信息和命令
    logger.info(f"表格数据源读取成为，内容为:\n{input_command_data}")

    """
    这里传参的逻辑是
    1. 优先从表格读取相应字段的数据   表格字段的名字可以在properties文件中的表格对应关系中定义
    2. 如果表格内容为空 则 从 properties中的默认元信息中读取
    3. 换言之 只有ip和cmdlist是必须在表格里存在的 否则报错
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i in range(len(input_command_data)):
            future = executor.submit(connect_and_execute,
                                     input_command_data[i].get(param.get("excel_cmd")).split("\n"),
                                     param.get("device_type") if input_command_data[i].get(
                                         param.get("excel_device_type")) != input_command_data[i].get(
                                         param.get("excel_device_type")) or
                                                                 input_command_data[i].get(
                                                                     param.get("excel_device_type")) is None else
                                     input_command_data[i].get(param.get("excel_device_type")),
                                     input_command_data[i].get(param.get("excel_ip")),
                                     param.get("username") if input_command_data[i].get(param.get("excel_username")) !=
                                                              input_command_data[i].get(
                                                                  param.get("excel_username")) or input_command_data[
                                                                  i].get(param.get("excel_username")) is None else
                                     input_command_data[i].get(param.get("excel_username")),
                                     param.get("password") if input_command_data[i].get(param.get("excel_password")) !=
                                                              input_command_data[i].get(
                                                                  param.get("excel_password")) or input_command_data[
                                                                  i].get(param.get("excel_password")) is None else
                                     input_command_data[i].get(param.get("excel_password")),
                                     retry,
                                     param.get("identity") if input_command_data[i].get(param.get("excel_identity")) !=
                                                              input_command_data[i].get(
                                                                  param.get("excel_identity")) or input_command_data[
                                                                  i].get(param.get("excel_identity")) is None else
                                     input_command_data[i].get(param.get("excel_identity")),
                                     param.get("enable_password") if input_command_data[i].get(
                                         param.get("excel_enable_password")) != input_command_data[i].get(
                                         param.get("excel_enable_password")) or input_command_data[i].get(
                                         param.get("excel_enable_password")) is None else input_command_data[i].get(
                                         param.get("excel_enable_password")),
                                     global_delay_factor,
                                     param.get("is_save") if input_command_data[i].get(param.get("excel_is_save")) !=
                                                             input_command_data[i].get(
                                                                 param.get("excel_is_save")) or input_command_data[
                                                                 i].get(param.get("excel_is_save")) is None else
                                     input_command_data[i].get(param.get("excel_is_save")),
                                     conn_timeout,
                                     timeout,
                                     session_log_path=OUT_PUT_PATH,
                                     reserved_keyword=i
                                     )
            futures.append(future)
        for future in futures:
            re = enhancement_method(future.result())
            logger.info(f"处理结果{re}")

    logger.info("-----------处理结束时长:" + str(time.time() - t1) + "----------------")
    print("执行完成，请按任意键退出...")
    input()  # 等待用户输入字符，按任意键退出
