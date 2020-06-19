from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from custom.models import Hospital
from custom.models import Corona_warrior
from custom.models import Area



#--------------------------------------------------------Index Page--------------------------------------------#

def index(request):
    return render(request, 'custom/first.html', {})

#--------------------------------------------------------Index Page--------------------------------------------#





#-------------------------------------------------Functions of GOD Official--------------------------------------------#



# home function for health-official 
@login_required(login_url="god_login/")
def god_home(request):
	user = request.user
	if(user.is_god==True):
		area_hospitals=Hospital.objects.filter(area__exact=user.area)

		ccc=Hospital.objects.filter(area__exact=user.area).filter(category__exact='COVID care centre')
		dchc=Hospital.objects.filter(area__exact=user.area).filter(category__exact='Dedicated COVID health centre')
		dch=Hospital.objects.filter(area__exact=user.area).filter(category__exact='Dedicated COVID hospital')

		working_cw=[]
		cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=False)
		for cw in cws:
			if cw.last_placed.area==user.area:
				working_cw.append(cw)
			
		q_cw=[]
		cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=True)
		for cw in cws:
			if cw.area==user.area:

				q_cw.append(cw)


		all_areas = Area.objects.all()		

		return render(request, 'custom/god_success.html', {'current_user':user, 'area_ccc':ccc,'area_dchc':dchc,'area_dch':dch,'w_cw':working_cw,'q_cw':q_cw, 'area_hospitals' :area_hospitals, 'all_areas':all_areas})    
	else:
		return render(request, 'custom/god_login.html', {})			


# health-offcical login function
def god_login(request):
    return render(request, 'custom/god_login.html', {})


# authorization function for health-official
def god_author(request):
	# all_hospitals = Hospital.objects.all()

	if(request.method=="POST"):
		username = request.POST['username']
		password = request.POST['password']
	else:
		u = request.user
		if u is not None:
			return render(request, 'custom/god_success.html', {'current_user':u, 'all':all_hospitals})	
		else:
			return render(request, 'custom/god_login.html', {})					

	#user authentication django in-built function		
	user = authenticate(username=username, password=password)
	
	if user is not None:
		if(user.is_god==True):


			login(request, user)

			area_hospitals=Hospital.objects.filter(area__exact=user.area)

			ccc=Hospital.objects.filter(area__exact=user.area).filter(category__exact='COVID care centre')
			dchc=Hospital.objects.filter(area__exact=user.area).filter(category__exact='Dedicated COVID health centre')
			dch=Hospital.objects.filter(area__exact=user.area).filter(category__exact='Dedicated COVID hospital')

			# working corona warriors
			working_cw=[]
			cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=False)
			for cw in cws:
				if cw.last_placed.area==user.area:
					working_cw.append(cw)

			
			# quarantined corona warriors		
			q_cw=[]
			cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=True)
			for cw in cws:
				if cw.area==user.area:

					q_cw.append(cw)

		
			all_areas = Area.objects.all()
			
			return render(request, 'custom/god_success.html', {'current_user':user, 'area_ccc':ccc,'area_dchc':dchc,'area_dch':dch,'w_cw':working_cw,'q_cw':q_cw, 'area_hospitals' :area_hospitals, 'all_areas':all_areas})
		else:
			return render(request, 'custom/god_failure.html', {})						
	else:
		return render(request, 'custom/god_failure.html', {})    

#registering corona warrior
def register(request):
	if(request.method=="POST"):
		warrior_name = request.POST['name']
		warrior_hosp_id = request.POST['hospital']	
		hospital = Hospital.objects.get(pk=warrior_hosp_id)

		new_warrior = Corona_warrior.objects.create(name=warrior_name, is_quarantined=False, last_placed=hospital, area=hospital.area,working_since=timezone.now())

		user = request.user

		area_hospitals=Hospital.objects.filter(area__exact=user.area)

		ccc=Hospital.objects.filter(area__exact=user.area).filter(category__exact='COVID care centre')
		dchc=Hospital.objects.filter(area__exact=user.area).filter(category__exact='Dedicated COVID health centre')
		dch=Hospital.objects.filter(area__exact=user.area).filter(category__exact='Dedicated COVID hospital')

		working_cw=[]
		cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=False)
		for cw in cws:
			if cw.last_placed.area==user.area:
				working_cw.append(cw)

			
		q_cw=[]
		cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=True)
		for cw in cws:
			if cw.area==user.area:

				q_cw.append(cw)

		all_areas = Area.objects.all()		

		return render(request, 'custom/god_success.html',{'current_user':user, 'area_ccc':ccc,'area_dchc':dchc,'area_dch':dch,'w_cw':working_cw,'q_cw':q_cw, 'area_hospitals' :area_hospitals, 'all_areas':all_areas} )		

# transferring corona warrior to another hospital
def transfer(request):
	if(request.method=="POST"):
		warrior_id = request.POST['cw_id']
		warrior_hosp_id = request.POST['hospital']	
		hospital = Hospital.objects.get(pk=warrior_hosp_id)

		current_warrior = Corona_warrior.objects.get(pk=warrior_id)

		current_warrior.is_quarantined = False
		current_warrior.quarantined_since = None
		current_warrior.last_placed = hospital
		current_warrior.working_since=timezone.now()

		current_warrior.save()

		user = request.user

		area_hospitals=Hospital.objects.filter(area__exact=user.area)

		ccc=Hospital.objects.filter(area__exact=user.area).filter(category__exact='COVID care centre')
		dchc=Hospital.objects.filter(area__exact=user.area).filter(category__exact='Dedicated COVID health centre')
		dch=Hospital.objects.filter(area__exact=user.area).filter(category__exact='Dedicated COVID hospital')

		working_cw=[]
		cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=False)
		for cw in cws:
			if cw.last_placed.area==user.area:
				working_cw.append(cw)

			
		q_cw=[]
		cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=True)
		for cw in cws:
			if cw.area==user.area:

				q_cw.append(cw)


		all_areas = Area.objects.all()		

		return render(request, 'custom/god_success.html',{'current_user':user, 'area_ccc':ccc,'area_dchc':dchc,'area_dch':dch,'w_cw':working_cw,'q_cw':q_cw, 'area_hospitals' :area_hospitals,'all_areas':all_areas} )

# transferring corona warrior to another area
def deport(request):
	if(request.method=="POST"):
		warrior_id = request.POST['cw_id']
		new_area_id = request.POST['new_area']	
		new_area = Area.objects.get(pk=new_area_id)

		current_warrior = Corona_warrior.objects.get(pk=warrior_id)

		current_warrior.area = new_area

		current_warrior.save()

		user = request.user

		area_hospitals=Hospital.objects.filter(area__exact=user.area)

		ccc=Hospital.objects.filter(area__exact=user.area).filter(category__exact='COVID care centre')
		dchc=Hospital.objects.filter(area__exact=user.area).filter(category__exact='Dedicated COVID health centre')
		dch=Hospital.objects.filter(area__exact=user.area).filter(category__exact='Dedicated COVID hospital')

		working_cw=[]
		cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=False)
		for cw in cws:
			if cw.last_placed.area==user.area:
				working_cw.append(cw)

			
		q_cw=[]
		cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=True)
		for cw in cws:
			if cw.area==user.area:

				q_cw.append(cw)


		all_areas = Area.objects.all()		


		return render(request, 'custom/god_success.html',{'current_user':user, 'area_ccc':ccc,'area_dchc':dchc,'area_dch':dch,'w_cw':working_cw,'q_cw':q_cw, 'area_hospitals' :area_hospitals, 'all_areas':all_areas} )

#-----------------------------------------------  Functions of GOD Official--------------------------------------------#

 
#---------------------------------------------------Common  Functions------------------------------------------#
def logout_karo(request):
	logout(request)
	return render(request, 'custom/first.html', {})		    	

@login_required
def change_pass_form(request):
	return render(request,'custom/change_pass_form.html')

def change_password(request):
	if(request.method=='POST'):
		old_pass=request.POST['old_pass']
		new_pass=request.POST['new_pass']
		conf_pass=request.POST['conf_pass']

		u=request.user	
		conf_u=authenticate(username=u.username,password=old_pass)
		if conf_u is None:
			return render(request,'custom/wrong_pass.html')
		else:
			if conf_pass==new_pass:
				conf_u.set_password(new_pass)
				conf_u.save()
				return render (request,'custom/pass_change_success.html',{'current_user':conf_u})
			else:
				return render(request,'custom/typo.html')
#---------------------------------------------------Common Functions------------------------------------------#


#-----------------------------------------------------Functions of SysAd--------------------------------------------#

# home function for sys-ad
@login_required(login_url="sys_login/")
def sys_home(request):
	user = request.user
	if(user.is_god==False):
		apna_hospital = user.hospital

		working_cw=[]
		cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=False)
		for cw in cws:
			if cw.last_placed==user.hospital:
				working_cw.append(cw)

		
		return render(request, 'custom/sys_success.html', {'current_user':user, 'apna_hospital':apna_hospital, 'w_cw':working_cw})
	else:
		return render(request, 'custom/sys_login.html', {})			

# login function for sys-ad
def sys_login(request):
    return render(request, 'custom/sys_login.html', {})

# authorization function for sys-ad
def sys_author(request):
	if(request.method=="POST"):
		username = request.POST['username']
		password = request.POST['password']
	else:
		user = request.user

		apna_hospital = user.hospital

		working_cw=[]
		cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=False)
		for cw in cws:
			if cw.last_placed==user.hospital:
				working_cw.append(cw)

		if user is not None:			
			return render(request, 'custom/sys_success.html', {'current_user':user, 'apna_hospital':apna_hospital, 'w_cw':working_cw})	
		else:
			return render(request, 'custom/sys_login.html', {})					

	user = authenticate(username=username, password=password)
	
	if user is not None:
		if(user.is_god!=True):
			login(request, user)

			apna_hospital = user.hospital

			working_cw=[]
			cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=False)
			for cw in cws:
				if cw.last_placed==user.hospital:
					working_cw.append(cw)



			return render(request, 'custom/sys_success.html', {'current_user':user, 'apna_hospital':apna_hospital, 'w_cw':working_cw })
		else:
			return render(request, 'custom/sys_failure.html', {})						
	else:
		return render(request, 'custom/sys_failure.html', {})	


# updating hospital database
def update(request):
	updated_patients = request.POST['patients']
	updated_beds = request.POST['beds']
	updated_ppe_kits = request.POST['ppe_kits']
	updated_masks = request.POST['masks']
	updated_icu_beds = request.POST['icu_beds']
	updated_ventilators = request.POST['ventilators']

	hospital_id = request.POST['h_id']
	hospital = Hospital.objects.get(pk=hospital_id)

	hospital.no_of_covid_patients = updated_patients
	hospital.no_of_beds = updated_beds
	hospital.no_of_ppe_kits = updated_ppe_kits
	hospital.no_of_masks = updated_masks
	hospital.no_of_icu_beds = updated_icu_beds
	hospital.no_of_ventilators = updated_ventilators


	hospital.save()

	user = request.user
	
	apna_hospital = user.hospital

	working_cw=[]
	cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=False)
	for cw in cws:
		if cw.last_placed==user.hospital:
			working_cw.append(cw)

	return render(request, 'custom/sys_success.html', {'current_user':user, 'apna_hospital':apna_hospital, 'w_cw':working_cw })

# corona warrior quarantine function
def quarantine(request):
	if request.method=="POST":	
		to_be_quarantined=request.POST['cw']
		q_cw=Corona_warrior.objects.get(pk=to_be_quarantined)
		q_cw.is_quarantined=True
		q_cw.quarantined_since=timezone.now()
		q_cw.working_since=None

		q_cw.save()
		
		user=request.user
		apna_hospital = user.hospital
		working_cw=[]
		cws=Corona_warrior.objects.select_related('last_placed').filter(is_quarantined__exact=False)
		for cw in cws:
			if cw.last_placed==user.hospital:
				working_cw.append(cw)



		return render(request, 'custom/sys_success.html', {'current_user':user, 'apna_hospital':apna_hospital, 'w_cw':working_cw })

#-----------------------------------------------------Functions of SysAd--------------------------------------------#




