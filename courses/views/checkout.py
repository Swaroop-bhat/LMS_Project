from django.shortcuts import render,redirect
from django.urls import path,include
from django.shortcuts import HttpResponse
from courses.models import Course,Video,Payment,UserCourse
from onlinelearning.settings import *
from time import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import razorpay

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

@login_required(login_url='/login')
def checkout(request,slug):
    course=Course.objects.get(slug=slug)
    user=request.user
    action=request.GET.get('action')
    order=None
    error=None
    payment=None
    print(user.username)
    try:
        user_course=UserCourse.objects.get(user=user,course=course)
        error="you are already enrolled this course"
    except:
        pass
    if error is None:   
        amount=int((course.price - (course.price * course.discount * 0.01))*100)
        currency="INR"
        notes={
            "email":user.email,
            "name":f'{user.username}'
            }
        receipt= f"onlinelearning-{int(time())}"
        order=client.order.create(
            {'receipt':receipt,
        'notes':notes,
        'amount':amount,
        'currency':currency
        })
        payment=Payment()
        payment.user=user
        payment.course=course
        payment.order_id=order.get('id')
        payment.status = 'created'
        payment.save()

    context={
        "course":course,
        "order":order,
        "payment":payment,
        "user":user,
        "error":error

    }
    return render(request,template_name='courses/check_out.html',
    context=context)
   
# @csrf_exempt   
# def verifyPayment(request):
#    if request.method=="POST":
#     data=request.POST
#     context={}
#     print(data)
#     try:
#         client.utility.verify_payment_signature(data)
#         razorpay_order_id=data['razorpay_order_id']
#         razorpay_payment_id=data['razorpay_payment_id']

#         payment=Payment.objects.get(order_id=razorpay_order_id)
#         payment.payment_id=razorpay_payment_id
#         payment.status=True

#         userCourse=userCourse(user=payment.user,course=payment.course)
#         userCourse=userCourse.save()
#         payment.user_course=userCourse
#         payment.save()
#         return render(request,template_name='courses/my_courses.html',
#            context=context)
#     except:
#         return HttpResponse("Invalid Payment details")    
@csrf_exempt   
def verifyPayment(request):
    print(request.method)
    if request.method == "GET":
        data = request.GET

        context = {}
        print(data) 
        try:
            # client.utility.verify_payment_signature(data)
            razorpay_order_id = data['order_id']
            razorpay_payment_id = data['payment_id']
            print(razorpay_order_id)
            print(razorpay_payment_id)
            print("HY1")
            payment = Payment.objects.get(order_id=razorpay_order_id)
            print("HY2")
            payment.payment_id = razorpay_payment_id
            payment.status = "success"

            userCourse = UserCourse.objects.create(user=payment.user, course=payment.course)
            payment.user_course = userCourse
            payment.save()

            subject = 'Course Enrollment Confirmation'
            message = f"Thank you for enrolling in the course '{payment.course.name}'."
            from_email = 'swaroopbhat12345@gmail.com'  
            to_email = payment.user.email

            email = EmailMessage(subject, message, from_email, [to_email])

            email.send()
            print("qawsedf")
            return redirect('my-courses')
        except razorpay.errors.SignatureVerificationError as e:
            return HttpResponse("Invalid Payment details: Signature Verification Error")
        except Payment.DoesNotExist:
            print(request.user.username)
            return HttpResponse("Invalid Payment details: Payment not found")
  