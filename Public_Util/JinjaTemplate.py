"""
 @author：     JiaGuo
 @emil：       1520047927@qq.com
 @date：       Created in 2025/3/31 17:36
 @description：
 @modified By：
 @version:     1.0
"""

from jinja2 import Template

from Public_Util import file_util


class JinjaTemplate:
    """
    jinja模板引擎
    """

    def template_render_for_file(self, file_name, **kwargs):
        """
        渲染模板
        :param file_name: 文件名
        :param kwargs: 参数
        :return:
        """
        con = file_util.get_file_content_toString(file_name)
        template = Template(con)
        return template.render(**kwargs)

    def template_render_for_string(self, string, **kwargs):
        """
        渲染模板
        :param string: 字符串
        :param kwargs: 参数
        :return:
        """
        template = Template(string)
        return template.render(**kwargs)
