from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Area model
class Area(models.Model):
	area_name = models.CharField(max_length=20)

	def __str__(self):
		return self.area_name

# Creating Hospital model
class Hospital(models.Model):
	name = models.CharField(max_length=50)


	area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True, default=None)

	no_of_covid_patients = models.IntegerField()
	no_of_beds = models.IntegerField()
	no_of_ppe_kits = models.IntegerField()
	no_of_masks = models.IntegerField()
	no_of_icu_beds=models.IntegerField(default='0')
	category_choices=(('COVID care centre','COVID care centre'),
				('Dedicated COVID health centre','Dedicated COVID health centre'),
				('Dedicated COVID hospital','Dedicated COVID hospital'))
	category=models.CharField(max_length=50,choices=category_choices,default='COVID care centre')
	no_of_ventilators=models.IntegerField(default='0')
	def __str__(self):
		return self.name + ", " + self.area.area_name
	REQUIRED_FIELDS=['name','area','category']

#Creating Custom User Manager
class MyOfficialManager(BaseUserManager):
	
	def create_user(self, username, name, password=None):
		if not username:
			raise ValueError("Users must have a username")
		if not name:
			raise ValueError("Users must have a name")

		user = self.model(
				username = username,
				name = name,	
			)			

		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self, username, name, password):
		user = self.create_user(
				username = username,
				name = name,
				password = password, 
			)	

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

# Creating Custom User
class Official(AbstractBaseUser):
	username = models.CharField(max_length=30, unique=True)
	name = models.CharField(max_length=30, unique=False)
	hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True, default=None)
	# h_id = models.IntegerField(default=0)
	is_god = models.BooleanField(default=False)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True, default=None)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['name']

	objects = MyOfficialManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True			

class Corona_warrior(models.Model):
	name=models.CharField(max_length=30)
	is_quarantined=models.BooleanField()
	quarantined_since=models.DateField(null=True,blank=True)
	working_since=models.DateField(null=True,blank=True)
	last_placed=models.ForeignKey(Hospital,on_delete=models.CASCADE)

	area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True, default=None)	
	
	def __str__(self):
		return self.name


