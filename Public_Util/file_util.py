"""
 @author：     JiaGuo
 @emil：       1520047927@qq.com
 @date：       Created in 2025/4/9 15:31
 @description：
 @modified By：
 @version:     1.0
"""
import json
import os


# 追加写入文件  文件名需要传参进去
def write_file_append(content, file_name):
    if isinstance(content, list):
        content = "\n".join(content)
    with open(file_name, "a") as f:
        f.write("" if content is None else content + "\n")
        f.close()



# 逐行读取文件去除结尾的换行符返回一个list
def read_file(file_name):
    temp = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f.readlines():
            temp.append(line.strip())
    f.close()
    return temp

# 遍历文件夹下的所有文件名
def get_all_files(path):
    """
    遍历文件夹下的所有文件名
    :param path: 文件夹路径
    :return: 文件名列表
    """
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def get_file_content_toJson(file_name):
    """
    juniper的 json格式读取和输出  默认是data文件夹下的内容
    :param file_name:
    :return:
    """
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        context = f.read().replace('\n', '').replace(' ', '')
        return json.loads(context)




def get_file_content_toList(file_name):
    """
    逐行读取和以List方式输出 去除句首空格 默认是data文件夹下的内容
    :param file_name:
    :return:
    """
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        context = f.readlines()
        return [i.strip() for i in context if i.strip() != '']



def get_file_content_toString(file_name):
    """
    逐行读取和以string方式输出 去除句首空格 默认是data文件夹下的内容
    :param file_name:
    :return:
    """
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        context = f.read()
        return context
