from django.db import models
from courses.models import Course
from courses.models import UserCourse
# from django.contrib.auth.models import User
from django.conf import settings
class Payment(models.Model):
    order_id=models.CharField(max_length=50,null=False)
    payment_id=models.CharField(max_length=50)
    user_course=models.ForeignKey(UserCourse,null=True,blank=True,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(null=True, blank=True, max_length=20)
    