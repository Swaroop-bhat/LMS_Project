from django import forms
from courses.models import Course, Tag, Prerequisites, Learning,Video

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields=['name','slug','description','price','discount','thumbnail','length']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class PrerequisitesForm(forms.ModelForm):
    class Meta:
        model = Prerequisites
        fields = '__all__'

class LearningForm(forms.ModelForm):
    class Meta:
        model = Learning
        fields = '__all__'

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'serial_number', 'video_id', 'is_preview']
