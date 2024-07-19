from django.contrib import admin
from .models import CustomUser,Patient,PDF,DoctorPatient
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(PDF)
admin.site.register(DoctorPatient)