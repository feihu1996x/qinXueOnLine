"""
@file: adminx.py
@brief: 
@author: feihu1996.cn
@date: 18-7-10 下午3:44
@version: 1.0
"""

import xadmin

from courses.models import Course, BannerCourse ,Chapter, Video, CourseResource


class ChapterInline:
    model = Chapter
    extra = 0


class CourseResourceInline:
    model = CourseResource
    extra = 0


class CourseAdmin:
    list_display = ['name', 'desc', 'detail', 'level', 'learning_time', 'students', 'fav_nums', 'cover_image', 'click_nums', 'add_time']
    # list_display.append('get_chapter_nums')  # 方法也可以跟普通字段一样被放进来
    # list_display.append('go_to')  # 在管理器中嵌入自定义的html代码
    search_fields = ['name', 'desc', 'detail', 'level', 'learning_time', 'students', 'fav_nums', 'cover_image', 'click_nums']
    list_filter = list_display
    model_icon = 'fa fa-binoculars'  # 设置管理器的icon图标，图标资源位于xadmin/static/xadmin/vendor/font-awesome
    # list_editable = ['level', 'desc']  # 设置level和desc字段可以在管理器的列表页直接被修改
    ordering = ['-click_nums']  # 设置条目按照'click_nums'字段值降序排列
    # readonly_fields = ['fav_nums']  # 设置'fav_num'字段为只读字段，即只能动态产生，不能在后台手动修改
    # exclude = ['click_nums']  # 设置'click_nums'字段不显示
    inlines = [ChapterInline, CourseResourceInline]  # 在课程的管理界面中内联章节和课程资源（只能实现一级内联）
    # refresh_times = [3, 5]  # 设置当前管理器页面的自动刷新频率（3秒或5秒）
    style_fields = {"detail": "ueditor"}  # 集成ueditor富文本(detail字段)(xadmin/plugins/ueditor.py)
    import_excel = True  # 只在课程管理器中激活excel导入插件(xadmin/plugins/excel.py)

    def queryset(self):
        queryset = super(CourseAdmin, self).queryset()
        queryset = queryset.filter(is_banner=False)  # 只显示非轮播图课程
        return queryset

    def save_models(self):
        """
        保存课程的时候，
        自动统计课程机构的课程数
        :return:
        """
        obj = self.new_obj  # 当前新增的Course实例
        obj.save()
        if obj.course_org:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        """
        处理excel文件（excel插件导入）
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if 'excel' in request.FILES:
            # 随意发挥，
            # 自定义处理excel文件的逻辑，
            # 保存到model的某个字段中
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin:
    list_display = ['name', 'desc', 'detail', 'level', 'learning_time', 'students', 'fav_nums', 'cover_image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'level', 'learning_time', 'students', 'fav_nums', 'cover_image', 'click_nums']
    list_filter = list_display
    model_icon = 'fa fa-binoculars'
    inlines = [ChapterInline, CourseResourceInline]  # 在课程的管理界面中内联章节和课程资源（只能实现一级内联）

    def queryset(self):
        queryset = super(BannerCourseAdmin, self).queryset()
        queryset = queryset.filter(is_banner=True)  # 只显示轮播图课程
        return queryset


class ChapterAdmin:
    list_display = ['course', 'chapter_name', 'add_time']
    search_fields = ['course', 'chapter_name']
    # course是外键，'course__name'则指明了将外键的name字段作为过滤字段
    list_filter =  ['course__name', 'chapter_name', 'add_time']
    model_icon = 'fa fa-address-card-o'


class VideoAdmin:
    list_display = ['chapter', 'video_name', 'add_time']
    search_fields = ['chapter', 'video_name']
    list_filter = ['chapter__chapter_name', 'video_name', 'add_time']
    model_icon = 'fa fa-file-movie-o'


class CourseResourceAdmin:
    list_display = ['course', 'resource_name', 'download', 'add_time']
    search_fields = ['course', 'resource_name', 'download']
    list_filter = ['course__name', 'resource_name', 'download', 'add_time']
    model_icon = 'fa fa-download'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
