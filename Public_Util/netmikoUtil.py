"""
 @author：     JiaGuo
 @emil：       1520047927@qq.com
 @date：       Created in 2025/4/9 13:47
 @description：
 @modified By：
 @version:     1.0
"""
import datetime
import os
import sys

from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import logging.handlers

from Public_Util.file_util import write_file_append

PATTERN = ""
ABSOLUTELYPATH = ''
# 获取当前项目的绝对路径
if getattr(sys, 'frozen', False):
    ABSOLUTELYPATH = os.path.dirname(sys.executable)
else:
    ABSOLUTELYPATH = os.path.dirname(os.path.abspath(__file__))
OUT_PUT_PATH = os.path.join(ABSOLUTELYPATH, 'logs')
if not os.path.exists(OUT_PUT_PATH):
    os.mkdir(OUT_PUT_PATH)
FILE_LOG_PATH = os.path.join(OUT_PUT_PATH,
                             "netmiko日志" + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".log")

# 设置日志
logger = logging.getLogger('netmiko日志')
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console)
filelog = logging.handlers.RotatingFileHandler(FILE_LOG_PATH, maxBytes=10 * 1024 * 1024, backupCount=5)
filelog.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
filelog.setLevel(logging.INFO)
logger.addHandler(filelog)

def connect_and_execute(cmds: list,
                        device_type: str,
                        ip: str,
                        username: str,
                        password: str,
                        retry: int = 3,
                        enable: str = 'user',
                        enable_password: str = None,
                        global_delay_factor: int = 1,
                        is_save: bool = False,
                        conn_timeout: int = 10,
                        timeout: int = 60,
                        session_log_path: str = None,
                        reserved_keyword = None
                        ):
    """
    连接设备并执行命令
    :param reserved_keyword:  预留参数 用于回传通信
    :param cmds:  需要执行的命令  列表形式
    :param device_type: 设备类型
    :param ip: 设备ip
    :param username: 用户名
    :param password: 密码
    :param retry: 重试次数
    :param enable: 是否进入特权模式 root 或者 user
    :param enable_password: 特权模式密码
    :param global_delay_factor: 全局延迟因子
    :param is_save: 是否保存配置
    :param conn_timeout: 连接超时时间
    :param timeout: 执行命令超时时间
    :param session_log_path: 会话日志文件路径
    :return:
    """
    while retry > 0:
        try:
            logger.info("正在处理:" + ip + "----------------------")
            with ConnectHandler(
                device_type=device_type,
                ip=ip,
                username=username,
                password=password,
                timeout=timeout,
                conn_timeout=conn_timeout,
                session_log=os.path.join(session_log_path, ip + ".txt") if session_log_path else None,
                secret= None if enable_password == '' else enable_password,
                global_delay_factor=global_delay_factor,
            ) as conn:
                output = ''
                if enable == 'root':
                    conn.enable()
                    output = conn.send_config_set(cmds, enter_config_mode=enable)
                else:
                    for cmd in cmds:
                        output += conn.send_command(cmd)
                try:
                    if is_save:
                        conn.save_config()
                except NotImplementedError as e:
                    logger.warning(f"{ip} 的设备不支持保存配置，错误信息: {e}")
                logger.info("处理结果" + output)
                return {"ip":ip,"data":output,"reserved_keyword":reserved_keyword}

        except NetmikoTimeoutException as e:
            retry -= 1
            logger.warning(f"TCP连接错误,连接{ip}，剩余重试次数: {retry}日志信息为{e}")
            if retry == 0:
                logger.error(f"{ip} 的连接失败，重试耗尽")
                write_file_append(ip, os.path.join(session_log_path, "error.txt"))
                logger.exception(e)
                return None

        except NetmikoAuthenticationException as e:
            logger.warning(f"用户名密码错误,连接{ip}，剩余重试次数: {retry}日志信息为{e}")
            logger.error(f"{ip} 的连接失败，重试耗尽")
            write_file_append(ip, os.path.join(session_log_path, "error.txt"))
            logger.exception(e)
            return None

        except Exception as e:
            retry -= 1
            logger.warning(f"兜底异常 ,连接{ip}，剩余重试次数: {retry}日志信息为{e}")
            if retry == 0:
                logger.error(f"{ip} 的连接失败，重试耗尽")
                write_file_append(ip, os.path.join(session_log_path, "error.txt"))
                logger.exception(e)
                return None
