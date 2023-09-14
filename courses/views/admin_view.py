from django.shortcuts import render,redirect
from courses.models import Course, Tag, Prerequisites, Learning
from courses.forms.forms import CourseForm, TagForm, PrerequisitesForm, LearningForm,VideoForm
from courses.models import Payment,User,UserCourse
from django.core.mail import send_mail



def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.added_by= request.user 
            course.save()  
            return redirect('display_course_details')
    else:
        form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form})


from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from courses.serializers import CourseSerializer
from courses.custom_permission import StudentRolePermission,TeacherRolePermission

@api_view(['POST'])
@permission_classes([StudentRolePermission])
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.data)
        if form.is_valid():
            course = form.save(commit=False)
            # course.added_by = request.user
            course.save()
            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_course_details')
    else:
        form = TagForm()
    return render(request, 'courses/add_tag.html', {'form': form})

def add_prerequisites(request):
    if request.method == 'POST':
        form = PrerequisitesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_course_details')
    else:
        form = PrerequisitesForm()
    return render(request, 'courses/add_prerequisites.html', {'form': form})


def add_learning(request):
    if request.method == 'POST':
        form = LearningForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_course_details')
    else:
        form = LearningForm()
    return render(request, 'courses/add_learning.html', {'form': form})



def add_video(request, course_id):
    course = Course.objects.get(id=course_id)
    
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course 
            video.save()
            return redirect('display_course_details')
    else:
        form = VideoForm()

    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'courses/add_video.html', context)


# # @teacher_required
# def add_video(request,id):
#     print("hello")
#     course=Course.objects.get(id=id)
#     user=request.user
#     if request.method == 'POST':
#         form = VideoForm(request.POST)
#         if form.is_valid():
#             video=form.save(commit=False)
#             video.course=course
#             video.save()
#             print("hello")
#             enrolled_students_emails=UserCourse.objects.filter(course=course).values_list('user',flat=True)
#             content=video.title
            
#             if enrolled_students_emails:
#                 email_subject = 'New Course Notification!'
#                 from_email = 'swaroopbhat12345@gmail.com'
#                 to_email_list = list(enrolled_students_emails)
#                 print(to_email_list)
#                 print("email sent")
                
#                 send_mail(
#                     email_subject,
#     f'''Dear Student,
    
#             {user} has added new Contents to The Course {course}
#             Check Out the latest Content:{content}
            
        
#     Regards Team OLP''',
#                     from_email,
#                     to_email_list,
#                     fail_silently=False,
#                 )
                
#             return redirect('display_course_details',id=course.id)
#     else:
#         print("email sent")
#         form = VideoForm()
#         context={'form': form,
#                 'course':course}
#     return render('courses/add_video.html',context)


def purchased_students(request, course_id):
    course = Course.objects.get(id=course_id)
    purchased_students_ids= Payment.objects.filter(course=course).values_list('user', flat=True)
    purchased_students = User.objects.filter(id__in=purchased_students_ids)
    
    return render(request, 'courses/purchased_students.html', {'course': course, 'purchased_students': purchased_students})

