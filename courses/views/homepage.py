from django.shortcuts import render
from django.urls import path,include
from django.shortcuts import HttpResponse
from courses.models import Course
from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import TemplateView
from courses.models import Course

from courses.models import Course



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from courses.models import Course  
from courses.decorators import student_required,teacher_required

def home(request):
    data=Course.objects.all()
    page=Paginator(data,3)
    page_list=request.GET.get('page')
    page=page.get_page(page_list) 
    context={"page":page}
    return render(request,"courses/home.html",context)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from courses.models import Course
from courses.serializers import CourseSerializer

@api_view(['GET'])
def course_list(request):
    data = Course.objects.all()
    serializer = CourseSerializer(data, many=True)
    return Response(serializer.data)


from rest_framework.decorators import api_view,permission_classes, authentication_classes
from rest_framework.response import Response
from courses.models import Course
from courses.serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

def filter(request):
    queryset = Course.objects.all()  
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price and max_price:
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'queryset': queryset,
        'request': request,
    }
    return render(request, 'courses/home.html', context)


class SearchCoursesView(TemplateView):
    template_name = 'courses/search_results.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            courses = Course.objects.filter(Q(name__iexact=query))
            context['courses'] = courses
            context['query'] = query
        return context


@api_view(['GET'])
def search_courses(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(Q(name__iexact=query))
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    else:
        return Response([])