from django.db import models
from django.contrib.auth.models import User,AbstractUser,AbstractBaseUser,PermissionsMixin
from django.utils import timezone

import uuid


class UserNew(AbstractUser):
	is_teacher = models.BooleanField(default=False)
	is_student = models.BooleanField(default=False)


class Year(models.Model):
	name = models.CharField(max_length=300, null=True)
	def __str__(self):

		return f'{self.name}'

class Major(models.Model):
	name = models.CharField(max_length=300, null=True)
	year = models.ManyToManyField(Year)
	def __str__(self):
		return self.name

class Post(models.Model):
	major = models.ForeignKey(Major , on_delete=models.CASCADE,null=True)
	name = models.CharField(max_length=200, null=True)
	def __str__(self):
		return f'{self.name}'

class Subject(models.Model):
	major = models.ForeignKey(Major , on_delete=models.CASCADE,null=True)
	year = models.ForeignKey(Year , on_delete=models.CASCADE,null=True)
	subject = models.CharField(max_length=200 , null=True)
	def __str__(self):
		return f'{self.major} => {self.year} => {self.subject}'

class Teacher(models.Model):
	user = models.OneToOneField(UserNew , on_delete=models.CASCADE ,related_name = 'teacher',primary_key=True)
	name = models.CharField(max_length=200 , null=True)
	major = models.ForeignKey(Major , on_delete=models.CASCADE,null=True)
	post =  models.ForeignKey(Post , on_delete=models.CASCADE,null=True)
	def __str__(self):
		return f'{self.name} => {self.major} => {self.post}'

class Student(models.Model):
	user = models.OneToOneField(UserNew , on_delete=models.CASCADE ,related_name = 'student',primary_key=True)
	name = models.CharField(max_length=200 , null=True)
	major = models.ForeignKey(Major , on_delete=models.CASCADE,null=True)
	year = models.ForeignKey(Year , on_delete=models.CASCADE,null=True)
	roll = models.CharField(max_length=200 , null=True)
	def __str__(self):
		return f'{self.name} => {self.major} => {self.year}'


class ClassRoom(models.Model):
	name = models.CharField(max_length=100,default = uuid.uuid4().hex[:6].upper(),editable = False)
	major = models.ForeignKey(Major , on_delete=models.CASCADE,null=True)
	year = models.ForeignKey(Year , on_delete=models.CASCADE,null=True)
	subject = models.ForeignKey(Subject , on_delete=models.CASCADE,null=True)
	teacher = models.ForeignKey(Teacher , on_delete=models.CASCADE,null=True)
	start = models.DateTimeField(auto_now_add=timezone.now)
	can_join = models.BooleanField(default=True)
	password = models.CharField(max_length=200,null=True)


class Join_Room(models.Model):
	class_rom = models.ForeignKey(ClassRoom , on_delete=models.CASCADE,null=True)
	student = models.ForeignKey(Student , on_delete=models.CASCADE,null=True)

	def __str__(self):
		return f'{self.student} => {self.class_rom}'
