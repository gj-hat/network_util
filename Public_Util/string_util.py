"""
 @author：     JiaGuo
 @emil：       1520047927@qq.com
 @date：       Created in 2025/4/1 15:36
 @description： 字符串奇奇怪怪处理工具类
 @modified By：
 @version:     1.0
"""


def filter_mark_key_by_list(key_list, mark_start, mark_end):
    """
    过滤标记符号
    例如 {{aa}} 只留下aa
    :param key_list: key list
    :return: 过滤后的key list
    """
    res = []
    for key in key_list:
        if isinstance(key, list):
            key = key[0]
        if check_is_mark(key, mark_start, mark_end):
            res.append(filter_mark_key(key, mark_start, mark_end))
    # res 去重空值
    return list(set(res))

    # return list(map(lambda key: (
    #     lambda k: filter_mark_key(k, mark_start, mark_end) if check_is_mark(k, mark_start, mark_end) else None)(
    #     key[0] if isinstance(key, list) else key), key_list))


def filter_mark_key(key, mark_start, mark_end):
    """
    过滤标记符号
    例如 {{aa}} 只留下aa
    :param mark_end:
    :param mark_start:
    :param key: key
    :return: 过滤后的key
    """
    return key.replace(mark_start, "").replace(mark_end, "").strip()


def check_is_mark(key, mark_start, mark_end):
    """
    判断是否是标记符号
    :param mark_end:
    :param mark_start:
    :param key: key
    :return: 是否是标记符号
    """
    return key.startswith(mark_start) and key.endswith(mark_end)

def add_mark(key, mark_start, mark_end):
    """
    添加标记符号
    :param mark_end:
    :param mark_start:
    :param key: key
    :return: 添加标记后的key
    """
    return mark_start + key + mark_end

if __name__ == '__main__':
    print(filter_mark_key("{{aa}}", "{{", "}}"))
    print(check_is_mark("{{aa}}", "{{", "}}"))
