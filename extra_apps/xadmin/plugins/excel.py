"""
@file: excel.py
@brief: 自定义xadmin插件——excel导入插件
@author: feihu1996.cn
@date: 18-7-17 下午2:19
@version: 1.0
"""

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader
from xadmin.plugins.utils import get_context_dict


class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)  # 返回True时才会加载此插件

    def block_top_toolbar(self, context, nodes):
        nodes.append(
            loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html',
                context=get_context_dict(context)))  # render_to_string会从xadmin/templates目录下找我们自定义的模板文件


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)
