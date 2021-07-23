from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .models import Teacher as Tea
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import RoomForm
from django.http import JsonResponse
import json
"""Login / out"""

def userLogin(request):
	if request.method == 'POST' or None:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('rollcall:home')
		else:
			messages.info(request,'Username or Password is incorrect..')
			return redirect('rollcall:login')

	return render(request, 'rollcall/login.html')


def userLogout(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('rollcall:login')

"""ENd Login / out"""




"""Home"""
@login_required(login_url='rollcall:login')
def home(request):
	user = request.user
	if request.user.is_student:

		student = Student.objects.get(user=user)
		if request.method == "POST":
			room_name = request.POST.get("room_name")
			room_password = request.POST.get("room_password")
			room_exi = ClassRoom.objects.filter(name=room_name)
			if room_exi:
				room = ClassRoom.objects.get(name=room_name)
				if room.can_join == True:
					if room.password == room_password and room.major == request.user.student.major and room.year == request.user.student.year:
						joined = Join_Room.objects.filter(class_rom=room,student=student).count()
						if joined == 0:
							return render(request,'rollcall/joinDetail.html',{'room':room})
						elif joined >= 1:
							messages = "You Are already joined"
							return render(request,'rollcall/error.html',{'messages':messages})
					else:
						if room.password != room_password:
							messages = "Password wrong"
							return render(request,'rollcall/error.html',{'messages':messages})
						else:
							messages = "You are not allowed"
							return render(request,'rollcall/error.html',{'messages':messages})
				else:
					messages = "This room is experied"
					return render(request,'rollcall/error.html',{'messages':messages})
			
			else:
				messages = "This room is not exist"
				return render(request,'rollcall/error.html',{'messages':messages})
		ctx = {'type':"std",'student':student}
		return render(request , 'rollcall/home.html',ctx)
	else:
		teacher = Teacher.objects.get(user=user)
		form = RoomForm()
		if request.method == "POST":
			form = RoomForm(request.POST)
			if form.is_valid():
				form.save()


		classroom = teacher.classroom_set.all() 
		ctx = {'classroom':classroom,'form':form,'teacher':teacher}
		return render(request , 'rollcall/home.html',ctx)

	
#8E1ABF
def join(request):
	data = json.loads(request.body)
	room = data['roomId']
	action = data['action']
	student = request.user.student
	if action == 'join':
		classroom = ClassRoom.objects.get(id=room)
		joined = Join_Room.objects.filter(class_rom=classroom,student=student).count()
		print(joined)
		if joined == 0:
			Join_Room.objects.create(class_rom=classroom, student=student)
			return HttpResponse('joined')

		else:
			return HttpResponse('shi')


	return JsonResponse('Item was added',safe=False)



def joined(request):


	return render(request , 'rollcall/joined.html')
"""End Home"""


"""Get Student in room"""

def classDetail(request , name):
	room_details = ClassRoom.objects.get(name=name)

	return render(request , 'rollcall/classDetail.html',{'room_details':room_details})

def getStudents(request , room):
	room_details = ClassRoom.objects.get(name=room)

	students_joined = room_details.join_room_set.all()
	students= []
	for i in students_joined:
		students.append({'name':i.student.name,'major':i.student.major.name,'roll':i.student.roll,'year':i.student.year.name})
	print(students)
	return JsonResponse({"student":students})

"""ENd """