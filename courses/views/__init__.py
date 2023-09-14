from courses.views.homepage import home,course_list,search_courses,SearchCoursesView,filter
from courses.views.courses import coursePage,MyCoursesList
from courses.views.auth import register_view,login_view,signout,teacher_signout,user_registration
from courses.views.checkout import checkout,verifyPayment
# from courses.views.display import display_course_details
from .display import display_course_details,delete_course,update_course,add_content,content_detail,update_video,delete_video
from courses.views.admin_view import add_course,add_learning,add_prerequisites,add_tag,add_video,purchased_students
from courses.views.reset import forgot_password_view,reset_password_view
from courses.views.rate_course import rate_course

# courses/views/__init__.py

