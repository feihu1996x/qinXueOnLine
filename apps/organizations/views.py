from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from organizations.models import CourseOrg, City, Teacher
from userOperations.models import UserFavorite
from courses.models import Course

from organizations.forms import UserAskModelForm


# Create your views here.
class OrgListView(View):
	"""
	课程机构列表请求处理类
	"""
	def get(self, request):
		all_orgs = CourseOrg.objects.all()  # 所有课程机构记录
		hot_orgs = all_orgs.order_by('-click_nums')[:3]  # 热门机构前三名（点击量）
		all_cities = City.objects.all()  # 所有城市记录

		# 课程机构记录筛选——city
		city_id = request.GET.get('city_id', '')
		if city_id:
			all_orgs = all_orgs.filter(city_id=city_id)

		# 课程机构记录筛选——category
		category = request.GET.get('category', '')
		if category:
			all_orgs = all_orgs.filter(category=category)

		# 总记录数
		org_nums = all_orgs.count()

		# 课程机构记录排序
		sort_by = request.GET.get('sort_by', '')
		if sort_by == 'student_nums':
			all_orgs = all_orgs.order_by('-student_nums')
		if sort_by == 'course_nums':
			all_orgs = all_orgs.order_by('-course_nums')

		# 对课程机构记录进行分页处理
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_orgs, 5, request=request)
		all_orgs = p.page(page)

		return render(request, 'org-list.html', {
			'all_orgs': all_orgs,
			'org_nums': org_nums,
			'all_cities': all_cities,
			'city_id': city_id,
			'category': category,
			'hot_orgs': hot_orgs,
			'sort_by': sort_by
		})


class UserAskView(View):
	"""
	用户咨询表单请求处理类
	"""
	def post(self, request):
		user_ask_model_form = UserAskModelForm(request.POST)

		if user_ask_model_form.is_valid():  # 表单字段验证通过
			user_ask_model_form.save(commit=True)  # 将POST过来的字段保存到数据库
			return HttpResponse('{"status": 0, "msg": "ok"}', content_type='application/json')  # 返回JSON数据，方便前端进行AJAX操作
		else:
			return HttpResponse('{"status": 1, "msg": "添加出错"}', content_type='application/json')


class OrgHomeView(View):
	"""
	机构首页请求处理类
	"""
	def get(self, request, org_id):
		current_page = 'home'
		course_org_record = CourseOrg.objects.get(id=int(org_id))
		all_course_records = course_org_record.course_set.all()[:3]
		all_teacher_records = course_org_record.teacher_set.all()[:1]

		# 判断用户的收藏状态
		has_fav = False
		if request.user.is_authenticated:  # 如果用户已经登录
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org_record.id, fav_type=2):  # 如果用户已经收藏
				has_fav = True

		return render(request, 'org-detail-homepage.html', {
			'course_org_record': course_org_record,
			'all_course_records': all_course_records,
			'all_teacher_records': all_teacher_records,
			'current_page': current_page,
			'has_fav': has_fav
		})


class OrgCourseView(View):
	"""
	机构课程请求处理类
	"""
	def get(self, request, org_id):
		current_page = 'course'
		course_org_record = CourseOrg.objects.get(id=int(org_id))
		all_course_records = course_org_record.course_set.all()

		# 判断用户的收藏状态
		has_fav = False
		if request.user.is_authenticated:  # 如果用户已经登录
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org_record.id, fav_type=2):  # 如果用户已经收藏
				has_fav = True

		return render(request, 'org-detail-course.html', {
			'course_org_record': course_org_record,
			'all_course_records': all_course_records,
			'current_page': current_page,
			'has_fav': has_fav
		})


class OrgDescView(View):
	"""
	机构详情请求处理类
	"""
	def get(self, request, org_id):
		current_page = 'desc'
		course_org_record = CourseOrg.objects.get(id=int(org_id))

		# 判断用户的收藏状态
		has_fav = False
		if request.user.is_authenticated:  # 如果用户已经登录
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org_record.id, fav_type=2):  # 如果用户已经收藏
				has_fav = True

		return render(request, 'org-detail-desc.html', {
			'course_org_record': course_org_record,
			'current_page': current_page,
			'has_fav': has_fav
		})


class OrgTeacherView(View):
	"""
	机构讲师请求处理类
	"""
	def get(self, request, org_id):
		current_page = 'teacher'
		course_org_record = CourseOrg.objects.get(id=int(org_id))
		all_teacher_records = course_org_record.teacher_set.all()

		# 判断用户的收藏状态
		has_fav = False
		if request.user.is_authenticated:  # 如果用户已经登录
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org_record.id, fav_type=2):  # 如果用户已经收藏
				has_fav = True

		return render(request, 'org-detail-teachers.html', {
			'course_org_record': course_org_record,
			'all_teacher_records': all_teacher_records,
			'current_page': current_page,
			'has_fav': has_fav
		})


class AddFavView(View):
	"""
	用户（取消）收藏请求处理类
	"""
	def post(self, request):
		fav_id = int(request.POST.get('fav_id', 0))
		fav_type = int(request.POST.get('fav_type', 0))

		if (not fav_id) or (not fav_type):
			return HttpResponse('{"status": 1, "msg": "参数错误"}', content_type='application/json')

		if not request.user.is_authenticated:
			return HttpResponse('{"status": 1, "msg": "用户未登录"}', content_type='application/json')

		exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
		if exist_records:  # 用户已经收藏
			exist_records.delete()  # 删除记录，即取消收藏
			return HttpResponse('{"status": 0, "msg": "收藏"}', content_type='application/json')
		else:
			user_fav_model = UserFavorite()
			user_fav_model.fav_id = fav_id
			user_fav_model.fav_type = fav_type
			user_fav_model.user = request.user
			user_fav_model.save()
			return HttpResponse('{"status": 0, "msg": "已收藏"}', content_type='application/json')


class TeacherListView(View):
	"""
	讲师列表请求处理类
	"""
	def get(self, request):
		all_teacher_records = Teacher.objects.all()
		hot_teacher_records = Teacher.objects.all().order_by("-fav_nums")[:3]
		teacher_nums = all_teacher_records.count()

		# 讲师列表记录排序
		sort_by = request.GET.get('sort_by', '')
		if sort_by == 'hot':
			all_teacher_records = all_teacher_records.order_by('-click_nums')

		# 对讲师记录进行分页处理
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_teacher_records, 5, request=request)
		all_teacher_records = p.page(page)

		return render(request, 'teachers-list.html', {
			'all_teacher_records': all_teacher_records,
			'sort_by': sort_by,
			'hot_teacher_records': hot_teacher_records,
			'teacher_nums': teacher_nums
		})


class TeacherDetailView(View):
	"""
	讲师详情请求处理类
	"""
	def get(self, request, teacher_id):
		teacher_record = Teacher.objects.get(id=int(teacher_id))
		all_teacher_courses = Course.objects.filter(teacher=teacher_record)
		hot_teacher_records = Teacher.objects.all().order_by("-fav_nums")[:3]

		# 判断讲师或者机构的收藏状态
		teacher_has_fav = False
		course_org_has_fav = False
		if request.user.is_authenticated:  # 如果用户已经登录
			if UserFavorite.objects.filter(user=request.user, fav_id=teacher_record.id, fav_type=3):  # 如果用户已经收藏该讲师
				teacher_has_fav = True
			if UserFavorite.objects.filter(user=request.user, fav_id=teacher_record.course_org.id, fav_type=2):  # 如果用户已经收藏该机构
				course_org_has_fav = True


		return render(request, 'teacher-detail.html', {
			"teacher_record": teacher_record,
			'all_teacher_courses': all_teacher_courses,
			'hot_teacher_records': hot_teacher_records,
			'teacher_has_fav': teacher_has_fav,
			'course_org_has_fav': course_org_has_fav
		})
