from django.contrib import admin
from django.urls import path,include
from courses.views import home,course_list,search_courses,filter,SearchCoursesView,coursePage,register_view,login_view,signout,checkout,verifyPayment,MyCoursesList,add_course,add_learning,add_prerequisites,add_tag,add_video,rate_course
from django.conf.urls.static import static
from .views import display_course_details,delete_course,update_course,add_content,content_detail,update_video,delete_video
from django.conf import settings
from courses.views.auth import login_view,otp_verification_view,teacher_signout,user_registration
from django.contrib.auth import views as auth_views

from courses.views import forgot_password_view,reset_password_view,purchased_students

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

urlpatterns = [
    path('',home,name='home'),
    path('filter/',filter,name="filter"),
    path('logout/',signout,name='logout'),
    path('teacher_logout/',teacher_signout,name='teacher_logout'),
    path('my-courses',MyCoursesList.as_view(),name='my-courses'),
    path('signup/',register_view,name='signup'),
    path('login/',login_view,name='login'),
    path('course/<str:slug>',coursePage,name='coursepage'),
    path('check-out/<str:slug>',checkout,name='checkoutpage'),
    path('verify_payment/',verifyPayment,name='verify_payment'),
    path('courses/', display_course_details, name='display_course_details'),
     path('add_course/', add_course, name='add-course'),
    path('add_tag/', add_tag, name='add-tag'),
    path('add_prerequisites/', add_prerequisites, name='add-prerequisites'),
    path('add_learning/', add_learning, name='add-learning'),
    path('add_video/',add_video,name="add-video"),
    path("otp-verification/",otp_verification_view,name="otp-verification"),
    path('search/', SearchCoursesView.as_view(), name='search-courses'),
    path('forget-password/',forgot_password_view,name="forget-password"),
    path('reset-password/<str:token>/',reset_password_view,name='reset-password'),
    path('delete-course/<int:course_id>/', delete_course, name='delete-course'),
    path('update-course/<int:course_id>/', update_course, name='update-course'),
    path('content/<int:course_id>/', content_detail, name='content-detail'),
    path('add-content/<int:course_id>/', add_content, name='add-content'),
    path('update-video/<int:video_id>/', update_video, name='update-video'),
    path('delete-video/<int:video_id>/', delete_video, name='delete-video'),
    path('rate-course/<str:course_slug>/', rate_course, name='rate_course'),
    path('course/<int:course_id>/purchased-students/', purchased_students, name='course-purchased-students'),


    # path('api/courses',course_list,name='course_list'),
    # path('api/search/',search_courses,name='search'),
    # path('api/register',user_registration,name="register"),

    path('api/gettoken/',TokenObtainPairView.as_view(),name="gettoken"),
    path('api/refreshtoken/',TokenRefreshView.as_view(),name="refreshtoken"),
    path('api/verifytoken/',TokenVerifyView.as_view(),name="verify"),


    path("api/courselist/",course_list,name="api_courselist"),
    path("api/addcourse/",add_course,name="api_addcourse"),

]  
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)