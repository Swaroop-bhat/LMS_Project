from django.shortcuts import redirect, get_object_or_404
from courses.models import Rating, Course

def rate_course(request, course_slug):
    if request.method == 'POST' and request.user.is_authenticated:
        rating_value = int(request.POST.get('rating'))
        course = get_object_or_404(Course, slug=course_slug)
        existing_rating = Rating.objects.filter(user=request.user, course=course).first()

        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.save()
        else:
            Rating.objects.create(
                user=request.user,
                course=course,
                rating=rating_value
            )
    return redirect('coursepage', slug=course_slug)
