
from rest_framework import serializers
from courses.models import Course,Video,User


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name','slug','description','price','discount','length','added_by')

        
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()