from django.db import models
from django.contrib.auth.models import User,AbstractUser,AbstractBaseUser,PermissionsMixin
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File 
from PIL import Image, ImageDraw
import uuid
import json
from ckeditor.fields import RichTextField

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
	


class Student(models.Model):
	user = models.OneToOneField(UserNew , on_delete=models.CASCADE ,related_name = 'student',primary_key=True)
	name = models.CharField(max_length=200 , null=True)
	major = models.ForeignKey(Major , on_delete=models.CASCADE,null=True)
	year = models.ForeignKey(Year , on_delete=models.CASCADE,null=True)
	roll = models.CharField(max_length=200 , null=True,unique=True)
	def __str__(self):
		return f'{self.name} => {self.major} => {self.year}'





class ClassRoom(models.Model):
	name = models.CharField(max_length=10,editable = False ,unique=True)
	major = models.ForeignKey(Major , on_delete=models.CASCADE,null=True)
	year = models.ForeignKey(Year , on_delete=models.CASCADE,null=True)
	subject = models.ForeignKey(Subject , on_delete=models.CASCADE,null=True)
	teacher = models.ForeignKey(Teacher , on_delete=models.CASCADE,null=True)
	start = models.DateTimeField(auto_now_add=timezone.now)
	can_join = models.BooleanField(default=True)
	password = models.CharField(max_length=200,null=True)
	qr_code = models.ImageField(upload_to='roomQr/',null=True,blank=True)

	def save(self,*args , **kwargs):
		
		if not self.name:
			self.name = uuid.uuid4().hex[:8].upper()
			while ClassRoom.objects.filter(name=self.name).exists():
				self.name = uuid.uuid4().hex[:8].upper()
		rawurl = {
				"name": str(self.name),
				"password": str(self.password)
		}
		url = json.dumps(rawurl)
		qrcode_image = qrcode.make(url)
		canvas = Image.new('RGB',(qrcode_image.pixel_size, qrcode_image.pixel_size),'white')
		draw = ImageDraw.Draw(canvas)
		canvas.paste(qrcode_image)
		fname = f'qrcode{self.name}.png'
		buff = BytesIO()
		canvas.save(buff,'PNG')
		self.qr_code.save(fname,File(buff),save=False)
		canvas.close()
		super().save(*args, **kwargs)

	    	

class Join_Room(models.Model):
	class_rom = models.ForeignKey(ClassRoom , on_delete=models.CASCADE,null=True)
	student = models.ForeignKey(Student , on_delete=models.CASCADE,null=True)

	def __str__(self):
		return f'{self.student} => {self.class_rom}'


class PostArticle(models.Model):
	post = models.ForeignKey(Teacher , on_delete=models.CASCADE,null=True,related_name='postarticle')
	content = RichTextField(blank=True,null=True)
	slug = models.CharField(max_length=10,editable = False ,unique=True)
	date = models.DateTimeField(auto_now_add=timezone.now)
	def save(self,*args , **kwargs):
		if not self.slug:
			self.slug = uuid.uuid4().hex[:10]
			while PostArticle.objects.filter(slug=self.slug).exists():
				self.slug = uuid.uuid4().hex[:10]
		super().save(*args, **kwargs)



