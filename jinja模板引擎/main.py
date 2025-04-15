"""
 @author：     JiaGuo
 @emil：       1520047927@qq.com
 @date：       Created in 2024/4/12 15:12
 @description：
 @modified By：
 @version:     1.0
"""
import os
import shutil
import sys



from Public_Util import string_util
from Public_Util.PropertiesReader import PropertiesReader
from Public_Util.excel_util import ExcelUtil, logger
from Public_Util.JinjaTemplate import JinjaTemplate



PATTERN = ""
ABSOLUTELYPATH = ''
# 获取当前项目的绝对路径
if getattr(sys, 'frozen', False):
    ABSOLUTELYPATH = os.path.dirname(sys.executable)
else:
    ABSOLUTELYPATH = os.path.dirname(os.path.abspath(__file__))
# 输出文件路径
OUT_PUT_PATH = os.path.join(ABSOLUTELYPATH, 'output')
LOGS_PATH = os.path.join(ABSOLUTELYPATH, 'logs')
DATA_PATH = os.path.join(ABSOLUTELYPATH, 'data')
TEMPLATE_PATH = os.path.join(ABSOLUTELYPATH, 'template')
"""
判断日志和输出文件夹是否存在，存在则删除 然后再添加
"""
if os.path.exists(OUT_PUT_PATH):
    shutil.rmtree(OUT_PUT_PATH)
os.mkdir(OUT_PUT_PATH)
if os.path.exists(LOGS_PATH):
    shutil.rmtree(LOGS_PATH)
os.mkdir(LOGS_PATH)
# 配置文件路径
PARAM_PATH = os.path.join(ABSOLUTELYPATH, 'config.properties')
# 数据文件路径
DATA_PATH = os.path.join(ABSOLUTELYPATH, 'data')
# 日志文件路径
FILE_LOG_PATH = os.path.join(LOGS_PATH, "控制台输出.log")
# 模板文件路径
TEMPLATE_FILE = os.path.join(TEMPLATE_PATH, "template")

JINJA_TEMPLATE = JinjaTemplate()

# 读取配置文件
PARA = PropertiesReader().read_properties(PARAM_PATH)



# 读取excel文件
def data_source_for_excel(file_path, sheet_name=PARA.get("SHEET_NAME"), row_num=0, col_num=1):
    """
    逐行读取excel文件
    :return:
    """
    excel_util = ExcelUtil(file_path)
    """
    读取数据源文件
    1. 读取表头 分为变量 和 关键字 两个列表
    2. 逐行读取数据
    3. 判断 有无模板列
    4. 判断有无模板文件
    5. 如果都没有则使用默认的模板文件
    """
    header = excel_util.get_header(sheet_name)
    variables_list = string_util.filter_mark_key_by_list(header,"{{","}}")
    key_list = string_util.filter_mark_key_by_list(header,"$","$")

    data_dict = excel_util.read_excel_dict(sheet_name)
    logger.info(f"读取数据源文件成功:{data_dict}")
    # print(data_dict)

    for i in range(len(data_dict)):
        # 构造变量字典，key 为变量名，value 为 record 中对应的值
        temp = {var: data_dict[i].get(string_util.add_mark(var, "{{", "}}")) for var in variables_list}
        result = ""
        if data_dict[i].get("$template$") == data_dict[i].get("$template$"):  # 使用模板表格文件
            # 从 data_dict[i] 中获取模板字符串（Excel 内含模板）
            template = data_dict[i].get("$template$")
            # 直接传入 temp 字典中的所有 key=value 作为 render 的参数
            result = JINJA_TEMPLATE.template_render_for_string(string = template, **temp)
            excel_util.write_excel_cell(sheet_name,i+2,PARA.get("res"),result)
        elif data_dict[i].get("$template_id$") == data_dict[i].get("$template_id$"):  # 使用模板表格文件 id是行号
            # 需要从另一个文件获取模板，此处预留处理逻辑
            pass
        else:  # 使用本地默认模板
            # 构造变量字典，key 为变量名，value 为 record 中对应的值
            temp = {var: data_dict[i].get(string_util.add_mark(var, "{{", "}}")) for var in variables_list}
            # 直接传入 temp 字典中的所有 key=value 作为 render 的参数
            result = JINJA_TEMPLATE.template_render_for_file(os.path.join(TEMPLATE_PATH, PARA.get("DEFULT_TEMPLATE_FILE")), **temp)
            # 将渲染结果写入excel当前行的$res$单元格里
            excel_util.write_excel_cell(sheet_name, i + 2, PARA.get("res"), result)


# 读取db
def data_source_for_db():
    pass



if __name__ == '__main__':

    data_source_type = PARA.get("DATA_SOURCE_TYPE")
    if data_source_type == "excel":
        data_source_for_excel(os.path.join(DATA_PATH, PARA.get("DATA_URL")))
        pass
    elif data_source_type == "db":
        pass
    else:
        print("不支持的数据源类型")
        sys.exit(1)

