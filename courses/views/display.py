from django.shortcuts import render,redirect
from django.http import HttpResponse
from courses.models import Course, Tag, Prerequisites, Learning,Video,User
from django.contrib.auth.decorators import login_required
from courses.decorators import student_required,teacher_required

# @login_required(login_url='/login')
@teacher_required
def display_course_details(request):
    user = request.user  
    courses = Course.objects.filter(added_by=user)
    tags = Tag.objects.all()
    prerequisites = Prerequisites.objects.all()
    learning = Learning.objects.all()
    video = Video.objects.all()

    context = {
        'courses': courses,
        'tags': tags,
        'prerequisites': prerequisites,
        'learning': learning,
        'video':video
    }
    return render(request,'courses/display.html',context)



from django.shortcuts import  get_object_or_404
@teacher_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, added_by=request.user)
    
    if request.method == 'POST':
        course.delete()
    
    return redirect('display_course_details')


from django.shortcuts import  get_object_or_404
from courses.forms.forms import CourseForm,VideoForm

@teacher_required
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, added_by=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('display_course_details')
    else:
        form = CourseForm(instance=course)

    context = {
        'form': form,
    }
    return render(request, 'courses/update_course.html', context)


# @teacher_required
# def add_content(request, course_id):
#     course = get_object_or_404(Course, id=course_id, added_by=request.user)

#     if request.method == 'POST':
#         form = VideoForm(request.POST)
#         if form.is_valid():
#             video = form.save(commit=False)
#             video.course = course
#             video.save()
#             return redirect('content-detail', course_id=course.id)
#     else:
#         form = VideoForm()

#     context = {
#         'form': form,
#         'course': course,
#     }
#     return render(request, 'courses/add_content.html', context)
from django.core.mail import send_mail

@teacher_required
def add_content(request, course_id):
    course = get_object_or_404(Course, id=course_id, added_by=request.user)

    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course
            video.save()

            purchased_users = User.objects.filter(usercourse__course=course)
            subject = 'New Content Added to {}'.format(course.name)
            message = 'New content has been added to the course: {}\n\nVisit the course page to see the new content.'.format(course.name)
            from_email = 'swaroopbhat12345"gmail.com'
            recipient_list = [user.email for user in purchased_users]

            send_mail(subject, message, from_email, recipient_list)

            return redirect('content-detail', course_id=course.id)
    else:
        form = VideoForm()

    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'courses/add_content.html', context)


from django.shortcuts import render, get_object_or_404
from courses.models import Video

@teacher_required
def content_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, added_by=request.user)
    videos = Video.objects.filter(course=course)

    context = {
        'course': course,
        'video': videos,
    }
    return render(request, 'courses/content_detail.html', context)


@teacher_required
def update_video(request, video_id):
    video = get_object_or_404(Video, id=video_id, course__added_by=request.user)

    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('content-detail', course_id=video.course.id)
    else:
        form = VideoForm(instance=video)

    context = {
        'form': form,
        'video': video,
        'course_id': video.course.id,
    }
    return render(request, 'courses/update_video.html', context)


@teacher_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id, course__added_by=request.user)

    if request.method == 'POST':
        video.delete()
    
    return redirect('content-detail', course_id=video.course.id)

