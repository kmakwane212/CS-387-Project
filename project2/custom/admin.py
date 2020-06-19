from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Hospital
from .models import Official
from .models import Corona_warrior
from .models import Area

# Register your models here.

class OfficialAdmin(UserAdmin):
	list_display = ('username', 'name', 'area', 'hospital', 'is_god', 'is_superuser')
	search_fields = ('username', 'name',)
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

class HospitalAdmin(admin.ModelAdmin):
	list_display = ('name', 'area', 'category')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

class WarriorAdmin(admin.ModelAdmin):
	list_display = ('name', 'is_quarantined', 'working_since','quarantined_since', 'last_placed', 'area',)
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Official, OfficialAdmin)
admin.site.register(Corona_warrior, WarriorAdmin)
admin.site.register(Area)
