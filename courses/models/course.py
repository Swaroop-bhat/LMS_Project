from django.db import models
from django.conf import settings
import courses.models
from PIL import Image

class Course(models.Model):
    name=models.CharField(max_length=50,null=False)
    slug=models.CharField(max_length=50,null=False,unique=True)
    description=models.CharField(max_length=200,null=True)
    price=models.IntegerField(max_length=200)
    discount=models.IntegerField(null=False,default=0)
    active=models.BooleanField(default=False)
    thumbnail=models.ImageField(upload_to="files/thumbnail")
    date=models.DateTimeField(auto_now_add=True)
    length=models.IntegerField(null=False)
    # added_by= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='0adec873-f6ce-4220-8a80-be3eb5b49274')
    added_by= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def average_rating(self):
        ratings = courses.models.Rating.objects.filter(course=self)
        if ratings:
            total_ratings = sum(rating.rating for rating in ratings)
            return total_ratings / len(ratings)
        return 0
    
    def save(self,*args, **kwargs):
        super(Course,self).save(*args,**kwargs)
        image=Image.open(self.thumbnail.path)

        if image.width>300 and image.height>300:
            output_size=(300,300)
            image.thumbnail(output_size)
            image.save(self.thumbnail.path)


class CourseProperty(models.Model):
    description=models.CharField(max_length=100,null=False)
    course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)

    class Meta:
        abstract=True

class Tag(CourseProperty):
    pass


class Prerequisites(CourseProperty):
   pass

class Learning(CourseProperty):
    pass