from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from courses.models import Course, CourseResource, Video
from userOperations.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.
class CourseListView(View):
	"""
	课程列表请求处理类
	"""
	def get(self, request):
		all_course_records = Course.objects.all().order_by('-add_time')  # 默认按课程添加时间从新到旧降序排列
		hot_course_records = all_course_records.order_by('-click_nums')[:3]

		# 课程记录排序
		sort_by = request.GET.get('sort_by', '')
		if sort_by == 'students':
			all_course_records = all_course_records.order_by('-students')
		if sort_by == 'click_nums':
			all_course_records = all_course_records.order_by('-click_nums')

		# 根据搜索关键词对课程记录进行筛选
		"""
		'name__icontains=search_keywords'的意思是，
		当name字段的值包含search_keywords时满足条件，
		'icontains'中的'i'表示不区分大小写
		"""
		search_keywords = request.GET.get('keywords', '')
		if search_keywords:
			all_course_records = all_course_records.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

		# 对课程记录进行分页处理
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_course_records, 6, request=request)
		all_course_records = p.page(page)

		return render(request, 'course-list.html', {
			'all_course_records': all_course_records,
			'sort_by': sort_by,
			'hot_course_records': hot_course_records
		})


class CourseDetailView(View):
	"""
	课程详情请求处理类
	"""
	def get(self, request, course_id):
		course_record = Course.objects.get(id=int(course_id))

		# 判断用户课程或者机构的收藏状态
		course_has_fav = False
		course_org_has_fav = False
		if request.user.is_authenticated:  # 如果用户已经登录
			if UserFavorite.objects.filter(user=request.user, fav_id=course_record.id, fav_type=1):  # 如果用户已经收藏该课程
				course_has_fav = True
			if UserFavorite.objects.filter(user=request.user, fav_id=course_record.course_org.id, fav_type=2):  # 如果用户已经收藏该机构
				course_org_has_fav = True

		# 增加课程点击数
		course_record.click_nums += 1
		course_record.save()

		related_courses = list()

		# 根据课程标签检索相似课程进行推荐
		course_tag = course_record.course_tag
		if course_tag:
			related_courses = Course.objects.filter(course_tag=course_tag)[:1]

		return render(request, 'course-detail.html', {
			'course_record': course_record,
			'related_courses': related_courses,
			'course_has_fav': course_has_fav,
			'course_org_has_fav': course_org_has_fav
		})


class CourseChapterView(LoginRequiredMixin, View):
	"""
	课程章节请求处理类
	"""
	def get(self, request, course_id):
		course_record = Course.objects.get(id=int(course_id))

		course_record.students += 1

		# 将当前登录用户和当前学习的课程关联起来
		user_course_records =  UserCourse.objects.filter(user=request.user, course=course_record)
		if not user_course_records:
			user_course_model = UserCourse(user=request.user, course=course_record)
			user_course_model.save()

		# 学习当前课程的同学还学习了哪些课程
		all_user_course_records_by_course = UserCourse.objects.filter(course=course_record)
		course_user_ids = [user_course_record.user.id for user_course_record in all_user_course_records_by_course]  # 学习过该课程的所有同学的id
		all_user_course_records_by_user_id =  UserCourse.objects.filter(user_id__in=course_user_ids)  # 'user_id__in=course_user_ids'表示只要user的id在id池中即满足条件
		user_course_ids = [user_course_record.course.id for user_course_record in all_user_course_records_by_user_id]  # 学习过该课程的所有同学学过的所有课程的id
		all_user_course_records = Course.objects.filter(id__in=user_course_ids).order_by('click_nums')[:5]  # 学习过该课程的所有同学学过的所有课程

		all_course_resources = CourseResource.objects.filter(course=course_record)
		return render(request, 'course-video.html', {
			'course_record': course_record,
			'all_course_resources': all_course_resources,
			'all_user_course_records': all_user_course_records
		})


class CourseCommentView(LoginRequiredMixin, View):
	"""
	课程评论请求处理函数
	"""
	def get(self, request, course_id):
		course_record = Course.objects.get(id=int(course_id))
		all_course_resources = CourseResource.objects.filter(course=course_record)
		all_course_comments = CourseComments.objects.filter(course=course_record)

		# 学习当前课程的同学还学习了哪些课程
		all_user_course_records_by_course = UserCourse.objects.filter(course=course_record)
		course_user_ids = [user_course_record.user.id for user_course_record in all_user_course_records_by_course]  # 学习过该课程的所有同学的id
		all_user_course_records_by_user_id =  UserCourse.objects.filter(user_id__in=course_user_ids)  # 'user_id__in=course_user_ids'表示只要user的id在id池中即满足条件
		user_course_ids = [user_course_record.course.id for user_course_record in all_user_course_records_by_user_id]  # 学习过该课程的所有同学学过的所有课程的id
		all_user_course_records = Course.objects.filter(id__in=user_course_ids).order_by('click_nums')[:5]  # 学习过该课程的所有同学学过的所有课程

		return render(request, 'course-comment.html', {
			'course_record': course_record,
			'all_course_resources': all_course_resources,
			'all_course_comments': all_course_comments,
			'all_user_course_records': all_user_course_records
		})

	def post(self, request, course_id):
		if not request.user.is_authenticated:
			return HttpResponse('{"status": 1, "msg": "用户未登录"}', content_type='application/json')

		course_id = int(course_id)
		course_comment = request.POST.get('course_comment', '')

		if course_id > 0 and course_comment:
			course_comment_model = CourseComments()
			course_comment_model.user = request.user
			course_comment_model.course = Course.objects.get(id=course_id)
			course_comment_model.comment_content = course_comment
			course_comment_model.save()
			return HttpResponse('{"status": 0, "msg": "评论提交成功"}', content_type='application/json')
		else:
			return HttpResponse('{"status": 1, "msg": "评论提交出错"}', content_type='application/json')


class CoursePlayView(LoginRequiredMixin, View):
	"""
	课程视频播放请求处理类
	"""
	def get(self, request, video_id):
		video_record = Video.objects.get(id=int(video_id))

		course_record = video_record.chapter.course

		# 学习当前课程的同学还学习了哪些课程
		all_user_course_records_by_course = UserCourse.objects.filter(course=course_record)
		course_user_ids = [user_course_record.user.id for user_course_record in all_user_course_records_by_course]  # 学习过该课程的所有同学的id
		all_user_course_records_by_user_id =  UserCourse.objects.filter(user_id__in=course_user_ids)  # 'user_id__in=course_user_ids'表示只要user的id在id池中即满足条件
		user_course_ids = [user_course_record.course.id for user_course_record in all_user_course_records_by_user_id]  # 学习过该课程的所有同学学过的所有课程的id
		all_user_course_records = Course.objects.filter(id__in=user_course_ids).order_by('click_nums')[:5]  # 学习过该课程的所有同学学过的所有课程

		all_course_resources = CourseResource.objects.filter(course=course_record)

		return render(request, 'course-play.html', {
			'course_record': course_record,
			'all_course_resources': all_course_resources,
			'all_user_course_records': all_user_course_records,
			'video_record': video_record
		})
