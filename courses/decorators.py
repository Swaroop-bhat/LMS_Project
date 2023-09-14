from django.http import HttpResponseForbidden
from functools import wraps
def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "teacher":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No access")

    return _wrapped_view

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "student":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No access")
   
    return _wrapped_view