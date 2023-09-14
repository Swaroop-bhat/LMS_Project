from django.db import models
from courses.models import Course
# from django.contrib.auth.models import User
# from courses.models import User
from django.conf import settings
# from django.contrib.auth import get_user_model
class UserCourse(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.course.name}'
